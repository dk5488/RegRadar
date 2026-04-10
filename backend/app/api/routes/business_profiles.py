"""
RegRadar — Business Profile Routes
CRUD for MSME business profiles (onboarding form).
Protected by JWT auth with owner/CA-firm scoping.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from typing import Optional
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.models import BusinessProfile, User
from app.models.enums import UserRole
from app.schemas.schemas import (
    BusinessProfileCreate, BusinessProfileUpdate,
    BusinessProfileResponse, PaginatedResponse,
)

router = APIRouter()


def _scoped_query(user: User):
    """
    Return a base query scoped to what the user is allowed to see:
    - ADMIN: all profiles
    - CA_FIRM_ADMIN / CA_REVIEWER: profiles belonging to their CA firm
    - MSME_OWNER: only their own profiles
    """
    query = select(BusinessProfile).where(BusinessProfile.is_active == True)

    if user.role == UserRole.ADMIN:
        return query
    elif user.role in (UserRole.CA_FIRM_ADMIN, UserRole.CA_REVIEWER):
        if user.ca_firm_id:
            return query.where(BusinessProfile.ca_firm_id == user.ca_firm_id)
        # CA user with no firm — see nothing
        return query.where(False)
    else:
        # MSME_OWNER — only their own profiles
        return query.where(BusinessProfile.owner_user_id == user.id)


@router.post("/", response_model=BusinessProfileResponse, status_code=201)
async def create_profile(
    profile_in: BusinessProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new MSME business profile (onboarding)."""
    profile = BusinessProfile(
        business_name=profile_in.business_name,
        business_type=profile_in.business_type,
        industry_sector=profile_in.industry_sector,
        industry_sector_other=profile_in.industry_sector_other,
        nic_code=profile_in.nic_code,
        registration_state=profile_in.registration_state,
        operating_states=[s.value for s in profile_in.operating_states],
        udyam_category=profile_in.udyam_category,
        employee_count_band=profile_in.employee_count_band,
        annual_turnover_band=profile_in.annual_turnover_band,
        gst_status=profile_in.gst_status,
        has_export_activity=profile_in.has_export_activity,
        has_manufacturing_unit=profile_in.has_manufacturing_unit,
        handles_food_products=profile_in.handles_food_products,
        existing_licences=[l.value for l in profile_in.existing_licences],
        preferred_language=profile_in.preferred_language,
        alert_channels=[c.value for c in profile_in.alert_channels],
        whatsapp_number=profile_in.whatsapp_number,
        email_address=profile_in.email_address,
        # Auto-set ownership
        owner_user_id=current_user.id,
    )

    # If the user belongs to a CA firm, link the profile to that firm
    if current_user.ca_firm_id:
        profile.ca_firm_id = current_user.ca_firm_id

    db.add(profile)
    await db.flush()
    await db.refresh(profile)
    return profile


@router.get("/", response_model=PaginatedResponse)
async def list_profiles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    ca_firm_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List business profiles with pagination (scoped to user's access)."""
    query = _scoped_query(current_user)

    # Admin or CA admin can further filter by a specific firm
    if ca_firm_id and current_user.role in (UserRole.ADMIN, UserRole.CA_FIRM_ADMIN):
        query = query.where(BusinessProfile.ca_firm_id == ca_firm_id)

    # Count
    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    # Paginate
    profiles = (
        await db.execute(
            query.offset((page - 1) * page_size).limit(page_size)
        )
    ).scalars().all()

    return PaginatedResponse(
        items=[BusinessProfileResponse.model_validate(p) for p in profiles],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.get("/{profile_id}", response_model=BusinessProfileResponse)
async def get_profile(
    profile_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a single business profile by ID."""
    query = _scoped_query(current_user).where(BusinessProfile.id == profile_id)
    result = await db.execute(query)
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.patch("/{profile_id}", response_model=BusinessProfileResponse)
async def update_profile(
    profile_id: UUID,
    update: BusinessProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Partially update a business profile."""
    query = _scoped_query(current_user).where(BusinessProfile.id == profile_id)
    result = await db.execute(query)
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = update.model_dump(exclude_unset=True)

    # Convert enum lists to string lists for JSONB fields
    if "operating_states" in update_data and update_data["operating_states"]:
        update_data["operating_states"] = [s.value for s in update_data["operating_states"]]
    if "existing_licences" in update_data and update_data["existing_licences"]:
        update_data["existing_licences"] = [l.value for l in update_data["existing_licences"]]
    if "alert_channels" in update_data and update_data["alert_channels"]:
        update_data["alert_channels"] = [c.value for c in update_data["alert_channels"]]

    for field, value in update_data.items():
        setattr(profile, field, value)

    await db.flush()
    await db.refresh(profile)
    return profile


@router.delete("/{profile_id}", status_code=204)
async def deactivate_profile(
    profile_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Soft-delete a business profile."""
    query = _scoped_query(current_user).where(BusinessProfile.id == profile_id)
    result = await db.execute(query)
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile.is_active = False
    await db.flush()

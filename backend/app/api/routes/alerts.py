"""
RegRadar — Alert Routes
User-facing alert inbox and acknowledgement.
Protected by JWT auth with owner/CA-firm scoping.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.models import Alert, BusinessProfile, User
from app.models.enums import AlertStatus, UserRole
from app.schemas.schemas import AlertResponse, AlertAcknowledge, PaginatedResponse

router = APIRouter()


def _scoped_alert_query(user: User):
    """
    Return a base alert query scoped to the user's access:
    - ADMIN: all alerts
    - CA roles: alerts for profiles under their firm
    - MSME_OWNER: alerts for their own profiles
    """
    query = select(Alert)

    if user.role == UserRole.ADMIN:
        return query
    elif user.role in (UserRole.CA_FIRM_ADMIN, UserRole.CA_REVIEWER):
        if user.ca_firm_id:
            return query.join(
                BusinessProfile, Alert.business_profile_id == BusinessProfile.id
            ).where(BusinessProfile.ca_firm_id == user.ca_firm_id)
        return query.where(False)
    else:
        # MSME_OWNER — only alerts for profiles they own
        return query.join(
            BusinessProfile, Alert.business_profile_id == BusinessProfile.id
        ).where(BusinessProfile.owner_user_id == user.id)


@router.get("/", response_model=PaginatedResponse)
async def list_alerts(
    business_profile_id: Optional[UUID] = None,
    status_filter: Optional[AlertStatus] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List alerts scoped to the authenticated user's access."""
    query = _scoped_alert_query(current_user)

    if business_profile_id:
        query = query.where(Alert.business_profile_id == business_profile_id)
    if status_filter:
        query = query.where(Alert.status == status_filter)

    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    alerts = (
        await db.execute(
            query.order_by(Alert.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).scalars().all()

    return PaginatedResponse(
        items=[AlertResponse.model_validate(a) for a in alerts],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = _scoped_alert_query(current_user).where(Alert.id == alert_id)
    result = await db.execute(query)
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/{alert_id}/acknowledge", response_model=AlertResponse)
async def acknowledge_alert(
    alert_id: UUID,
    ack: AlertAcknowledge,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark an alert as noted, done, or not applicable."""
    query = _scoped_alert_query(current_user).where(Alert.id == alert_id)
    result = await db.execute(query)
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    allowed_statuses = {
        AlertStatus.ACKNOWLEDGED_NOTED,
        AlertStatus.ACKNOWLEDGED_DONE,
        AlertStatus.ACKNOWLEDGED_NOT_APPLICABLE,
    }
    if ack.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Status must be one of: {', '.join(s.value for s in allowed_statuses)}",
        )

    alert.status = ack.status
    alert.acknowledgement_note = ack.note
    alert.acknowledged_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(alert)
    return alert

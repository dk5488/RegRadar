"""
RegRadar — CA Dashboard Routes
Endpoints for CA firms to manage their client portfolio.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from app.core.database import get_db
from app.models.models import (
    CAFirm, BusinessProfile, Alert, Document, ComplianceItem,
)
from app.models.enums import AlertStatus, DocumentStatus
from app.schemas.schemas import CAFirmCreate, CAFirmResponse

router = APIRouter()


@router.post("/firms", response_model=CAFirmResponse, status_code=201)
async def create_ca_firm(
    firm_in: CAFirmCreate, db: AsyncSession = Depends(get_db)
):
    """Register a new CA firm."""
    firm = CAFirm(**firm_in.model_dump())
    db.add(firm)
    await db.flush()
    await db.refresh(firm)
    return firm


@router.get("/firms/{firm_id}", response_model=CAFirmResponse)
async def get_ca_firm(firm_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CAFirm).where(CAFirm.id == firm_id))
    firm = result.scalar_one_or_none()
    if not firm:
        raise HTTPException(status_code=404, detail="CA Firm not found")
    return firm


@router.get("/firms/{firm_id}/dashboard")
async def ca_firm_dashboard(firm_id: UUID, db: AsyncSession = Depends(get_db)):
    """Dashboard summary for a CA firm — client count, pending alerts, etc."""
    # Verify firm exists
    result = await db.execute(select(CAFirm).where(CAFirm.id == firm_id))
    firm = result.scalar_one_or_none()
    if not firm:
        raise HTTPException(status_code=404, detail="CA Firm not found")

    # Client count
    client_count = (
        await db.execute(
            select(func.count())
            .select_from(BusinessProfile)
            .where(
                BusinessProfile.ca_firm_id == firm_id,
                BusinessProfile.is_active == True,
            )
        )
    ).scalar() or 0

    # Pending alerts across all clients
    pending_alerts = (
        await db.execute(
            select(func.count())
            .select_from(Alert)
            .join(BusinessProfile, Alert.business_profile_id == BusinessProfile.id)
            .where(
                BusinessProfile.ca_firm_id == firm_id,
                Alert.status == AlertStatus.PENDING,
            )
        )
    ).scalar() or 0

    # Documents awaiting review
    docs_pending_review = (
        await db.execute(
            select(func.count())
            .select_from(Document)
            .where(Document.status == DocumentStatus.REVIEW_PENDING)
        )
    ).scalar() or 0

    # Acknowledged alerts
    acknowledged = (
        await db.execute(
            select(func.count())
            .select_from(Alert)
            .join(BusinessProfile, Alert.business_profile_id == BusinessProfile.id)
            .where(
                BusinessProfile.ca_firm_id == firm_id,
                Alert.status.in_([
                    AlertStatus.ACKNOWLEDGED_NOTED,
                    AlertStatus.ACKNOWLEDGED_DONE,
                    AlertStatus.ACKNOWLEDGED_NOT_APPLICABLE,
                ]),
            )
        )
    ).scalar() or 0

    return {
        "firm_name": firm.firm_name,
        "subscription_tier": firm.subscription_tier.value,
        "max_client_profiles": firm.max_client_profiles,
        "active_clients": client_count,
        "pending_alerts": pending_alerts,
        "acknowledged_alerts": acknowledged,
        "documents_pending_review": docs_pending_review,
    }

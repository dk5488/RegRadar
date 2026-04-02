"""
RegRadar — Alert Routes
User-facing alert inbox and acknowledgement.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from app.core.database import get_db
from app.models.models import Alert
from app.models.enums import AlertStatus
from app.schemas.schemas import AlertResponse, AlertAcknowledge, PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
async def list_alerts(
    business_profile_id: Optional[UUID] = None,
    status_filter: Optional[AlertStatus] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List alerts for a business profile."""
    query = select(Alert)

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
async def get_alert(alert_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/{alert_id}/acknowledge", response_model=AlertResponse)
async def acknowledge_alert(
    alert_id: UUID,
    ack: AlertAcknowledge,
    db: AsyncSession = Depends(get_db),
):
    """Mark an alert as noted, done, or not applicable."""
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
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

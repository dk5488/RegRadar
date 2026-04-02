"""
RegRadar — Compliance Item Routes
CRUD for the applicability matrix entries.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from typing import Optional
from app.core.database import get_db
from app.models.models import ComplianceItem
from app.models.enums import UrgencyLevel
from app.schemas.schemas import (
    ComplianceItemCreate, ComplianceItemResponse, PaginatedResponse,
)

router = APIRouter()


@router.post("/", response_model=ComplianceItemResponse, status_code=201)
async def create_compliance_item(
    item_in: ComplianceItemCreate,
    db: AsyncSession = Depends(get_db),
):
    """Add a new compliance item to the applicability matrix."""
    # Check unique compliance_id
    existing = await db.execute(
        select(ComplianceItem).where(
            ComplianceItem.compliance_id == item_in.compliance_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=409, detail=f"Compliance ID '{item_in.compliance_id}' already exists"
        )

    item = ComplianceItem(**item_in.model_dump())
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.get("/", response_model=PaginatedResponse)
async def list_compliance_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    regulatory_body: Optional[str] = None,
    urgency_level: Optional[UrgencyLevel] = None,
    verified_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """List compliance items with filters."""
    query = select(ComplianceItem).where(ComplianceItem.is_active == True)

    if regulatory_body:
        query = query.where(ComplianceItem.regulatory_body == regulatory_body)
    if urgency_level:
        query = query.where(ComplianceItem.urgency_level == urgency_level)
    if verified_only:
        query = query.where(ComplianceItem.is_verified == True)

    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    items = (
        await db.execute(
            query.order_by(ComplianceItem.compliance_deadline.asc().nullslast())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).scalars().all()

    return PaginatedResponse(
        items=[ComplianceItemResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.get("/{item_id}", response_model=ComplianceItemResponse)
async def get_compliance_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ComplianceItem).where(ComplianceItem.id == item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Compliance item not found")
    return item

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.deps import require_admin
from app.models.models import Source, ScraperRun, User
from app.schemas.schemas import SourceHealthResponse, ScraperRunResponse, PaginatedResponse

router = APIRouter()

@router.get("/sources", response_model=List[SourceHealthResponse])
async def list_sources_health(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """List health status of all registered regulatory sources."""
    result = await db.execute(select(Source).order_by(Source.name))
    sources = result.scalars().all()
    return sources

@router.get("/runs", response_model=PaginatedResponse)
async def list_scraper_runs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    source_id: UUID = None,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """List historical runs of scrapers."""
    query = select(ScraperRun)
    if source_id:
        query = query.where(ScraperRun.source_id == source_id)
        
    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0
    
    runs = (
        await db.execute(
            query.order_by(ScraperRun.started_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).scalars().all()
    
    return PaginatedResponse(
        items=[ScraperRunResponse.model_validate(r) for r in runs],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )

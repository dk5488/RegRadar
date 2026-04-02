"""
RegRadar — Document Routes
View fetched documents and their LLM extraction results.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from app.core.database import get_db
from app.models.models import Document
from app.models.enums import DocumentStatus
from app.schemas.schemas import DocumentResponse, DocumentReview, PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
async def list_documents(
    status_filter: Optional[DocumentStatus] = None,
    source_id: Optional[UUID] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List fetched regulatory documents."""
    query = select(Document)

    if status_filter:
        query = query.where(Document.status == status_filter)
    if source_id:
        query = query.where(Document.source_id == source_id)

    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    docs = (
        await db.execute(
            query.order_by(Document.fetched_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).scalars().all()

    return PaginatedResponse(
        items=[DocumentResponse.model_validate(d) for d in docs],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.get("/{doc_id}", response_model=DocumentResponse)
async def get_document(doc_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.post("/{doc_id}/review", response_model=DocumentResponse)
async def review_document(
    doc_id: UUID,
    review: DocumentReview,
    db: AsyncSession = Depends(get_db),
):
    """CA reviewer approves, edits, or rejects a processed document."""
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if doc.status != DocumentStatus.REVIEW_PENDING:
        raise HTTPException(
            status_code=400,
            detail=f"Document is in '{doc.status.value}' state, not 'review_pending'",
        )

    if review.action == "approve":
        doc.status = DocumentStatus.APPROVED
        doc.approved_extraction = doc.llm_extraction
    elif review.action == "edit":
        if not review.edited_extraction:
            raise HTTPException(status_code=400, detail="edited_extraction required for edit action")
        doc.status = DocumentStatus.APPROVED
        doc.approved_extraction = review.edited_extraction
    elif review.action == "reject":
        doc.status = DocumentStatus.REJECTED
    else:
        raise HTTPException(status_code=400, detail="action must be: approve, edit, or reject")

    doc.review_notes = review.review_notes
    doc.reviewed_at = datetime.now(timezone.utc)
    # TODO: set reviewer_id from auth context
    await db.flush()
    await db.refresh(doc)
    return doc

"""
RegRadar — Celery Tasks
Section 6: Async task pipeline connecting all 7 stages of the compliance flow.

Tasks:
  1. process_document — LLM extraction on a fetched document (Stage 4)
  2. generate_alerts_for_item — Applicability matching + alert creation (Stage 6-7)
  3. deliver_alert_task — Multi-channel delivery for a single alert (Stage 7)
  4. run_scraper — Execute a source scraper (Stage 1-2)
"""

import asyncio
from uuid import UUID
from datetime import datetime, timezone

from app.core.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.core.logging import get_logger

logger = get_logger(__name__)


def _run_async(coro):
    """Helper to run async code inside sync Celery tasks."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ── Task 1: LLM Document Processing (Stage 4) ────────────────────────

@celery_app.task(
    name="regradar.process_document",
    bind=True,
    max_retries=2,
    default_retry_delay=60,
    rate_limit="50/h",  # Section 8: max 50 LLM requests/hour
)
def process_document(self, document_id: str):
    """
    Process a fetched document through the LLM extraction pipeline.

    Flow:
      1. Load document from DB
      2. Check status is 'extracted' or 'fetched'
      3. Send raw_text to LLM for structured extraction
      4. Store LLM extraction result + confidence score
      5. Set status to 'review_pending' (triggers CA review queue)
      6. If confidence < 0.75, mark for priority review (Section 12)
    """
    return _run_async(_process_document_async(self, document_id))


async def _process_document_async(task, document_id: str):
    from sqlalchemy import select
    from app.models.models import Document, Source
    from app.models.enums import DocumentStatus
    from app.services.llm_processor import extract_regulatory_content

    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                select(Document).where(Document.id == document_id)
            )
            doc = result.scalar_one_or_none()
            if not doc:
                logger.error("Document not found", document_id=document_id)
                return {"error": "Document not found"}

            if doc.status not in (DocumentStatus.FETCHED, DocumentStatus.EXTRACTED):
                logger.info(
                    "Document already processed, skipping",
                    document_id=document_id,
                    status=doc.status.value,
                )
                return {"skipped": True, "status": doc.status.value}

            # Update status to processing
            doc.status = DocumentStatus.PROCESSING
            await db.flush()

            # Get source name for the prompt
            source_result = await db.execute(
                select(Source).where(Source.id == doc.source_id)
            )
            source = source_result.scalar_one_or_none()
            source_name = source.name if source else "Unknown Source"

            # Run LLM extraction
            extraction = await extract_regulatory_content(
                raw_text=doc.raw_text or "",
                source_name=source_name,
                document_date=doc.fetched_at.strftime("%Y-%m-%d") if doc.fetched_at else "Unknown",
            )

            # Store results
            doc.llm_extraction = extraction.model_dump()
            doc.confidence_score = extraction.confidence_score
            doc.status = DocumentStatus.REVIEW_PENDING
            doc.processed_at = datetime.now(timezone.utc)

            await db.commit()

            logger.info(
                "Document processed successfully",
                document_id=document_id,
                title=extraction.title,
                confidence=extraction.confidence_score,
                priority_review=extraction.confidence_score is not None and extraction.confidence_score < 0.75,
            )

            return {
                "document_id": document_id,
                "title": extraction.title,
                "confidence": extraction.confidence_score,
            }

        except Exception as e:
            doc.status = DocumentStatus.FAILED
            doc.processing_error = str(e)
            await db.commit()
            logger.error("Document processing failed", document_id=document_id, error=str(e))
            raise task.retry(exc=e)


# ── Task 2: Alert Generation (Stage 6-7) ─────────────────────────────

@celery_app.task(
    name="regradar.generate_alerts",
    bind=True,
    max_retries=2,
    default_retry_delay=120,
)
def generate_alerts_for_item(self, compliance_item_id: str):
    """
    Run applicability matching for a compliance item and generate alerts.

    Called after a document is approved by a CA reviewer.
    """
    return _run_async(_generate_alerts_async(self, compliance_item_id))


async def _generate_alerts_async(task, compliance_item_id: str):
    from sqlalchemy import select
    from app.models.models import ComplianceItem
    from app.services.alert_generator import generate_alerts_for_compliance_item

    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                select(ComplianceItem).where(ComplianceItem.id == compliance_item_id)
            )
            item = result.scalar_one_or_none()
            if not item:
                return {"error": "Compliance item not found"}

            alerts = await generate_alerts_for_compliance_item(item, db)
            await db.commit()

            # Enqueue delivery for each alert
            for alert in alerts:
                deliver_alert_task.delay(str(alert.id))

            return {
                "compliance_item_id": compliance_item_id,
                "alerts_created": len(alerts),
            }

        except Exception as e:
            await db.rollback()
            logger.error("Alert generation failed", item_id=compliance_item_id, error=str(e))
            raise task.retry(exc=e)


# ── Task 3: Alert Delivery (Stage 7) ──────────────────────────────────

@celery_app.task(
    name="regradar.deliver_alert",
    bind=True,
    max_retries=3,
    default_retry_delay=300,
)
def deliver_alert_task(self, alert_id: str):
    """
    Deliver an alert via all configured channels.
    Creates DeliveryLog entries and dispatches to each channel.
    """
    return _run_async(_deliver_alert_async(self, alert_id))


async def _deliver_alert_async(task, alert_id: str):
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from app.models.models import Alert, BusinessProfile, DeliveryLog
    from app.services.alert_generator import create_delivery_logs_for_alert
    from app.services.delivery import deliver_alert

    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                select(Alert).where(Alert.id == alert_id)
            )
            alert = result.scalar_one_or_none()
            if not alert:
                return {"error": "Alert not found"}

            # Get the business profile for channel info
            profile_result = await db.execute(
                select(BusinessProfile).where(
                    BusinessProfile.id == alert.business_profile_id
                )
            )
            profile = profile_result.scalar_one_or_none()
            if not profile:
                return {"error": "Business profile not found"}

            # Create delivery logs if not already created
            logs_result = await db.execute(
                select(DeliveryLog).where(DeliveryLog.alert_id == alert.id)
            )
            existing_logs = logs_result.scalars().all()

            if not existing_logs:
                logs = await create_delivery_logs_for_alert(alert, profile, db)
            else:
                # Retry only failed logs
                logs = [l for l in existing_logs if l.failed_at and l.retry_count < 3]

            # Deliver via each channel
            results = []
            for log in logs:
                success = await deliver_alert(log, alert, db)
                results.append({"channel": log.channel.value, "success": success})

            await db.commit()

            return {
                "alert_id": alert_id,
                "deliveries": results,
            }

        except Exception as e:
            await db.rollback()
            logger.error("Alert delivery failed", alert_id=alert_id, error=str(e))
            raise task.retry(exc=e)


# ── Task 4: Run Scraper (Stage 1-2) ──────────────────────────────────

@celery_app.task(
    name="regradar.run_scraper",
    bind=True,
    max_retries=1,
    default_retry_delay=600,
)
def run_scraper(self, source_id: str):
    """
    Execute a scraper for a specific source — fetches new documents,
    checks for changes, and enqueues new docs for LLM processing.
    """
    return _run_async(_run_scraper_async(self, source_id))


async def _run_scraper_async(task, source_id: str):
    from sqlalchemy import select
    from app.models.models import Source, Document, ScraperRun
    from app.models.enums import DocumentStatus

    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                select(Source).where(Source.id == source_id)
            )
            source = result.scalar_one_or_none()
            if not source:
                return {"error": "Source not found"}

            # Create a ScraperRun record
            run = ScraperRun(
                source_id=source.id,
                started_at=datetime.now(timezone.utc),
            )
            db.add(run)
            await db.flush()

            # Dynamically load the scraper module
            try:
                scraper = _get_scraper_instance(source)
            except Exception as e:
                run.success = False
                run.error_message = f"Failed to load scraper: {e}"
                run.finished_at = datetime.now(timezone.utc)
                await db.commit()
                return {"error": str(e)}

            # Fetch documents
            raw_docs = await scraper.fetch()

            new_count = 0
            changed_count = 0

            for raw_doc in raw_docs:
                # Check if URL already exists
                existing_result = await db.execute(
                    select(Document).where(
                        Document.source_id == source.id,
                        Document.url == raw_doc.url,
                    )
                )
                existing_doc = existing_result.scalar_one_or_none()

                content_hash = scraper.compute_hash(raw_doc.raw_text or "")

                if existing_doc:
                    if existing_doc.content_hash == content_hash:
                        continue  # No change
                    # Content changed
                    existing_doc.previous_hash = existing_doc.content_hash
                    existing_doc.content_hash = content_hash
                    existing_doc.raw_text = raw_doc.raw_text
                    existing_doc.last_changed_at = datetime.now(timezone.utc)
                    existing_doc.status = DocumentStatus.FETCHED
                    changed_count += 1
                    # Re-queue for processing
                    process_document.delay(str(existing_doc.id))
                else:
                    # New document
                    doc = Document(
                        source_id=source.id,
                        url=raw_doc.url,
                        title=raw_doc.title,
                        raw_text=raw_doc.raw_text,
                        content_hash=content_hash,
                        status=DocumentStatus.FETCHED,
                    )
                    db.add(doc)
                    await db.flush()
                    new_count += 1
                    # Queue for processing
                    process_document.delay(str(doc.id))

            # Update source health
            source.last_fetched_at = datetime.now(timezone.utc)
            source.last_successful_fetch_at = datetime.now(timezone.utc)
            source.consecutive_failures = 0
            source.last_error = None

            # Complete the run record
            run.success = True
            run.documents_found = len(raw_docs)
            run.new_documents = new_count
            run.changed_documents = changed_count
            run.finished_at = datetime.now(timezone.utc)
            run.duration_seconds = (
                run.finished_at - run.started_at
            ).total_seconds()

            await scraper.close()
            await db.commit()

            logger.info(
                "Scraper run complete",
                source=source.name,
                found=len(raw_docs),
                new=new_count,
                changed=changed_count,
            )

            return {
                "source": source.name,
                "documents_found": len(raw_docs),
                "new": new_count,
                "changed": changed_count,
            }

        except Exception as e:
            source.consecutive_failures = (source.consecutive_failures or 0) + 1
            source.last_error = str(e)
            source.last_fetched_at = datetime.now(timezone.utc)

            run.success = False
            run.error_message = str(e)
            run.finished_at = datetime.now(timezone.utc)

            await db.commit()
            logger.error("Scraper run failed", source=source.name, error=str(e))
            raise task.retry(exc=e)


def _get_scraper_instance(source):
    """
    Dynamically resolve and instantiate the scraper class for a source.
    Maps scraper_module_name to the actual scraper class.
    """
    from app.core.config import get_settings
    settings = get_settings()

    # Scraper registry — maps module names to classes
    SCRAPER_REGISTRY = {}

    # Try to import central scrapers
    try:
        from app.scrapers.central.cbic_scraper import CBICScraper
        SCRAPER_REGISTRY["cbic_scraper"] = CBICScraper
    except ImportError:
        pass

    try:
        from app.scrapers.central.mca_scraper import MCAScraper
        SCRAPER_REGISTRY["mca_scraper"] = MCAScraper
    except ImportError:
        pass

    try:
        from app.scrapers.central.rbi_scraper import RBIScraper
        SCRAPER_REGISTRY["rbi_scraper"] = RBIScraper
    except ImportError:
        pass

    try:
        from app.scrapers.state.karnataka_scraper import KarnatakaScraper
        SCRAPER_REGISTRY["karnataka_scraper"] = KarnatakaScraper
    except ImportError:
        pass

    try:
        from app.scrapers.state.karnataka_scraper import KarnatakaScraper
        SCRAPER_REGISTRY["karnataka_scraper"] = KarnatakaScraper
    except ImportError:
        pass

    try:
        from app.scrapers.state.maharashtra_scraper import MaharashtraScraper
        SCRAPER_REGISTRY["maharashtra_scraper"] = MaharashtraScraper
    except ImportError:
        pass

    try:
        from app.scrapers.central.sebi_scraper import SEBIScraper
        from app.scrapers.central.epfo_scraper import EPFOScraper
        from app.scrapers.central.esic_scraper import ESICScraper
        from app.scrapers.central.labour_central_scraper import LabourCentralScraper
        from app.scrapers.central.dpiit_scraper import DPIITScraper
        from app.scrapers.central.incometax_scraper import IncomeTaxScraper
        from app.scrapers.central.gazette_scraper import GazetteScraper
        from app.scrapers.central.dgft_scraper import DGFTScraper
        from app.scrapers.central.fssai_scraper import FSSAIScraper
        from app.scrapers.central.bis_scraper import BISScraper
        from app.scrapers.central.irdai_scraper import IRDAIScraper
        from app.scrapers.state.tamilnadu_scraper import TamilNaduScraper
        from app.scrapers.state.delhi_scraper import DelhiScraper
        from app.scrapers.state.gujarat_scraper import GujaratScraper
        from app.scrapers.state.uttarpradesh_scraper import UttarPradeshScraper

        SCRAPER_REGISTRY['sebi_scraper'] = SEBIScraper
        SCRAPER_REGISTRY['epfo_scraper'] = EPFOScraper
        SCRAPER_REGISTRY['esic_scraper'] = ESICScraper
        SCRAPER_REGISTRY['labour_central_scraper'] = LabourCentralScraper
        SCRAPER_REGISTRY['dpiit_scraper'] = DPIITScraper
        SCRAPER_REGISTRY['incometax_scraper'] = IncomeTaxScraper
        SCRAPER_REGISTRY['gazette_scraper'] = GazetteScraper
        SCRAPER_REGISTRY['dgft_scraper'] = DGFTScraper
        SCRAPER_REGISTRY['fssai_scraper'] = FSSAIScraper
        SCRAPER_REGISTRY['bis_scraper'] = BISScraper
        SCRAPER_REGISTRY['irdai_scraper'] = IRDAIScraper
        SCRAPER_REGISTRY['tamilnadu_scraper'] = TamilNaduScraper
        SCRAPER_REGISTRY['delhi_scraper'] = DelhiScraper
        SCRAPER_REGISTRY['gujarat_scraper'] = GujaratScraper
        SCRAPER_REGISTRY['uttarpradesh_scraper'] = UttarPradeshScraper
    except ImportError:
        pass

    module_name = source.scraper_module_name
    scraper_class = SCRAPER_REGISTRY.get(module_name)

    if not scraper_class:
        raise ValueError(f"No scraper registered for module: {module_name}")

    return scraper_class(proxy_url=settings.PROXY_URL or None)

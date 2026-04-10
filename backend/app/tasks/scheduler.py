"""
RegRadar — Scraper Scheduler
Section 6, Component 1: Scheduled fetch jobs using APScheduler.
Schedules each active source based on its fetch_frequency_hours.

Run: python -m app.tasks.scheduler
"""

import asyncio
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.logging import setup_logging, get_logger
from app.models.models import Source

logger = get_logger(__name__)


async def schedule_all_scrapers():
    """
    Load all active sources from DB and schedule their scrapers.
    Section 8: "Schedule scrapes during off-peak hours (05:00–09:00 IST)"
    """
    setup_logging()

    scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Source).where(Source.is_active == True)
        )
        sources = result.scalars().all()

    if not sources:
        logger.warning("No active sources found in database. Run seeds first.")
        return

    for source in sources:
        # Import here to avoid circular imports
        from app.tasks import run_scraper

        scheduler.add_job(
            func=lambda sid=str(source.id): run_scraper.delay(sid),
            trigger=IntervalTrigger(hours=source.fetch_frequency_hours),
            id=f"scraper_{source.short_code}",
            name=f"Scraper: {source.name}",
            replace_existing=True,
        )

        logger.info(
            "Scheduled scraper",
            source=source.name,
            frequency_hours=source.fetch_frequency_hours,
        )

    scheduler.start()
    logger.info("Scheduler started", total_sources=len(sources))

    # Keep running
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    asyncio.run(schedule_all_scrapers())

"""
RegRadar — Manual Run All Scrapers
Trigger all active scrapers sequentially for testing.
"""

import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.models import Source
from app.tasks import run_scraper

async def run_all():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Source).where(Source.is_active == True)
        )
        sources = result.scalars().all()
    
    print(f"--- Found {len(sources)} active sources ---")
    
    for source in sources:
        print(f"Triggering: {source.name} ({source.short_code})...")
        # Trigger Celery task
        run_scraper.delay(str(source.id))
    
    print("--- All scrapers have been enqueued for execution ---")

if __name__ == "__main__":
    asyncio.run(run_all())

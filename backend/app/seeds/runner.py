"""
RegRadar — Seed Runner
Populates the database with initial master data (Sources, Compliance Items).
"""

import asyncio
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.logging import setup_logging, get_logger
from app.models.models import Source
from app.seeds.sources import REGULATORY_SOURCES

logger = get_logger(__name__)


async def seed_sources():
    """Seed the Source table with central and state regulatory bodies."""
    async with AsyncSessionLocal() as db:
        seeded_count = 0
        all_sources_data = REGULATORY_SOURCES

        for source_data in all_sources_data:
            # Check if source already exists by name
            result = await db.execute(
                select(Source).where(Source.name == source_data["name"])
            )
            existing = result.scalar_one_or_none()

            if not existing:
                source = Source(**source_data)
                db.add(source)
                seeded_count += 1
            else:
                # Update existing source just in case URLs/frequenies changed
                for key, value in source_data.items():
                    setattr(existing, key, value)

        await db.commit()
        logger.info(f"Seeded {seeded_count} new sources. Total sources updated: {len(all_sources_data)}")


async def main():
    setup_logging()
    logger.info("Starting database seed process...")
    
    await seed_sources()
    
    logger.info("Database seeding complete!")


if __name__ == "__main__":
    asyncio.run(main())

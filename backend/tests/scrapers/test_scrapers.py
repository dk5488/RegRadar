import asyncio
from app.scrapers.central.mca_scraper import MCAScraper
from app.scrapers.central.cbic_scraper import CBICScraper
from app.scrapers.central.rbi_scraper import RBIScraper
from app.scrapers.state.karnataka_scraper import KarnatakaScraper
from app.scrapers.state.maharashtra_scraper import MaharashtraScraper

async def run_scraper(scraper_class):
    print(f"\n--- Testing {scraper_class.__name__} ---")
    scraper = scraper_class()
    try:
        documents = await scraper.fetch()
        print(f"Found {len(documents)} documents.")
        for i, doc in enumerate(documents[:3]):
            print(f"  {i+1}. {doc.title[:80]}... - {doc.url}")
        if len(documents) > 3:
            print(f"  ... and {len(documents) - 3} more.")
    except Exception as e:
        print(f"Error running {scraper_class.__name__}: {e}")
    finally:
        await scraper.close()

async def main():
    scrapers = [
        MCAScraper,
        CBICScraper,
        RBIScraper,
        KarnatakaScraper,
        MaharashtraScraper,
    ]
    
    for scraper in scrapers:
        await run_scraper(scraper)

if __name__ == "__main__":
    asyncio.run(main())

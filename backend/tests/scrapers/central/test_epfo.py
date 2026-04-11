import asyncio
import traceback
import sys
import os

# Add backend to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.scrapers.central.epfo_scraper import EPFOScraper

async def main():
    print("Testing EPFO Scraper isolated...")
    scraper = EPFOScraper()
    try:
        documents = await scraper.fetch()
        print(f"Total Unique Documents: {len(documents)}")
        for i, doc in enumerate(documents[:5]):
            print(f" {i+1}. {doc.title} -> {doc.url}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(main())

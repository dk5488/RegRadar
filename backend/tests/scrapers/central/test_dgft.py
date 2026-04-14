
import asyncio
import traceback
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.scrapers.central.dgft_scraper import DGFTScraper

async def test_dgft():
    print("Testing DGFT Scraper isolated...")
    scraper = DGFTScraper()
    try:
        documents = await scraper.fetch()
        print(f"Total Unique Documents: {len(documents)}")
        for i, doc in enumerate(documents[:10]):
            print(f" {i+1}. {doc.title} -> {doc.url}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(test_dgft())

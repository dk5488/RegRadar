import asyncio
import traceback
from app.scrapers.central.mca_scraper import MCAScraper

async def main():
    print("Testing MCA Scraper isolated...")
    scraper = MCAScraper()
    try:
        documents = await scraper.fetch()
        print(f"Total Unique Documents: {len(documents)}")
        for doc in documents[:5]:
            print(f" - {doc.title} -> {doc.url}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(main())

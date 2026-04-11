import asyncio
import traceback
from app.scrapers.central.rbi_scraper import RBIScraper

async def main():
    print("Testing RBI Scraper isolated...")
    scraper = RBIScraper()
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

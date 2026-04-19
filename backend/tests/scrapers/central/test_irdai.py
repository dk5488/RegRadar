"""
F-16: IRDAI (Insurance Regulatory) Scraper — Isolated Test
"""
import asyncio
import traceback
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.scrapers.central.irdai_scraper import IRDAIScraper


async def main():
    print("=" * 60)
    print("Testing IRDAI Scraper")
    print("=" * 60)
    scraper = IRDAIScraper()
    try:
        documents = await scraper.fetch()
        print(f"\nTotal Unique Documents: {len(documents)}")
        for i, doc in enumerate(documents[:10]):
            safe_title = doc.title.encode("ascii", "replace").decode()
            print(f"  {i+1}. [{doc.content_type}] {safe_title}")
            print(f"     URL: {doc.url[:120]}")
        if len(documents) == 0:
            print("  WARNING: No documents returned!")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())

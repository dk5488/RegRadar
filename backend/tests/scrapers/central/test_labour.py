"""
F-19: Labour Central Scraper — Isolated Test
"""
import asyncio
import traceback
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.scrapers.central.labour_central_scraper import LabourCentralScraper


async def main():
    print("=" * 60)
    print("Testing Ministry of Labour Scraper")
    print("=" * 60)
    scraper = LabourCentralScraper()
    try:
        documents = await scraper.fetch()
        print(f"\nTotal Unique Documents: {len(documents)}")
        if len(documents) == 0:
            print("\nWARNING: No documents returned!")
            print("Reason: labour.gov.in utilizes a Next.js Client-Side SPA.")
            print("The site hydrates via JS; static requests yield empty DOMs.")
            print("Requires Playwright/Selenium integration for pipeline extraction.")
        else:
            for i, doc in enumerate(documents[:10]):
                safe_title = doc.title.encode("ascii", "replace").decode() if doc.title else "Untitled"
                print(f"  {i+1}. [{doc.content_type}] {safe_title}")
                print(f"     URL: {doc.url[:120]}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())

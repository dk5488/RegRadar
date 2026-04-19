"""
F-18: DPIIT Scraper — Isolated Test
"""
import asyncio
import traceback
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.scrapers.central.dpiit_scraper import DPIITScraper


async def main():
    print("=" * 60)
    print("Testing DPIIT Scraper")
    print("=" * 60)
    scraper = DPIITScraper()
    try:
        documents = await scraper.fetch()
        print(f"\nTotal Unique Documents: {len(documents)}")
        if len(documents) == 0:
            print("\nWARNING: No documents returned!")
            print("Reason: dpiit.gov.in utilizes a Next.js Single Page Application (SPA).")
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

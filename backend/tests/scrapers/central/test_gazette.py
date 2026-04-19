"""
F-17: Gazette Scraper — Isolated Test
"""
import asyncio
import traceback
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.scrapers.central.gazette_scraper import GazetteScraper


async def main():
    print("=" * 60)
    print("Testing Gazette of India Scraper")
    print("=" * 60)
    scraper = GazetteScraper()
    try:
        documents = await scraper.fetch()
        print(f"\nTotal Unique Documents: {len(documents)}")
        if len(documents) == 0:
            print("\nWARNING: No documents returned!")
            print("Reason: egazette.gov.in uses legacy ASP.NET WebForms containing hidden __VIEWSTATE tokens.")
            print("To extract PDFs, a headless browser (Playwright/Selenium) or complex POST token emulation is required.")
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

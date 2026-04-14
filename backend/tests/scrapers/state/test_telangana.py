"""
F-26: Telangana Scraper — Isolated Test
"""
import asyncio
import traceback
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.scrapers.state.telangana_scraper import TelanganaScraper

async def main():
    print("=" * 60)
    print("Testing Telangana State Scraper")
    print("=" * 60)
    scraper = TelanganaScraper()
    try:
        documents = await scraper.fetch()
        print(f"\nTotal Unique Documents: {len(documents)}")
        if len(documents) == 0:
            print("\nWARNING: No documents returned!")
        else:
            seen = set()
            deduped = []
            for doc in documents:
                if doc.url not in seen:
                    seen.add(doc.url)
                    deduped.append(doc)

            for i, doc in enumerate(deduped[:15]):
                safe_title = doc.title.encode("ascii", "replace").decode() if doc.title else "Untitled"
                safe_url = doc.url.encode("ascii", "replace").decode()
                print(f"  {i+1}. [{doc.content_type}] {safe_title}")
                print(f"     URL: {safe_url[:120]}")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(main())

"""
F-27: Andhra Pradesh Scraper — Isolated Test
"""
import asyncio
import traceback
import sys
import os

# Ensure app is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.scrapers.state.andhra_pradesh_scraper import AndhraPradeshScraper


async def main():
    print("=" * 60)
    print("Testing Andhra Pradesh State Scraper")
    print("=" * 60)
    scraper = AndhraPradeshScraper()
    try:
        documents = await scraper.fetch()
        print(f"\nTotal Unique Documents: {len(documents)}")
        if len(documents) == 0:
            print("\nWARNING: No documents returned!")
        else:
            for i, doc in enumerate(documents[:15]):
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

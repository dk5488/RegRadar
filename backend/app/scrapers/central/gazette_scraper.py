"""
RegRadar — Gazette Scraper
The official Gazette of India portal is built on legacy ASP.NET WebForms.
It relies heavily on POST requests with hidden __VIEWSTATE and __EVENTVALIDATION tokens
to navigate and render data tables. A pure GET-based scraper cannot natively parse its PDFs.
This scraper is a gracefully failing stub that logs the architectural limitation,
ready to be upgraded when a headless browser pipeline (Playwright/Selenium) is integrated.
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)


class GazetteScraper(BaseScraper):
    source_name = "Gazette of India"
    base_url = "https://egazette.gov.in"
    fetch_frequency_hours = 24
    requires_pdf_extraction = True

    async def fetch(self) -> List[RawDocument]:
        documents = []
        try:
            # We attempt the root request
            response = await self.safe_get(self.base_url)
            soup = BeautifulSoup(response.text, "lxml")
            
            pdf_links = soup.find_all("a", href=lambda href: href and ".pdf" in href.lower())
            
            if not pdf_links:
                logger.warning("Gazette ASP.NET block detected. No PDF links exposed in raw HTML payload.")
                # We do not crash, we return empty list so the orchestrator knows 0 docs were fetched.
                return documents
                
            for link in pdf_links:
                href = link.get("href", "")
                title = link.get_text(strip=True)[:200]
                
                if self.is_valuable_compliance_document(title, href):
                    full_url = href if href.startswith("http") else f"{self.base_url.rstrip('/')}/{href.lstrip('/')}"
                    documents.append(RawDocument(
                        url=full_url,
                        title=title,
                        raw_text=title,
                        content_type="application/pdf"
                    ))
                    
            logger.info("GazetteScraper fetch complete", doc_count=len(documents))
        except Exception as e:
            logger.error(f"Failed to fetch GazetteScraper", error=str(e))
            
        return documents

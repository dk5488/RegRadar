"""
RegRadar — LabourCentralScraper
The Ministry of Labour and Employment site (labour.gov.in)
is built on a Next.js Client-Side Rendering (CSR) framework (similar to DPIIT).
The dynamic PDF grids are not rendered in the HTTP payload. 
This scraper flags the SPA requirement and halts gracefully.
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)


class LabourCentralScraper(BaseScraper):
    source_name = "Ministry of Labour and Employment"
    base_url = "https://labour.gov.in/notifications"
    fetch_frequency_hours = 24
    requires_pdf_extraction = True

    async def fetch(self) -> List[RawDocument]:
        documents = []
        try:
            response = await self.safe_get(self.base_url)
            soup = BeautifulSoup(response.text, "lxml")
            
            pdf_links = soup.find_all("a", href=lambda href: href and ".pdf" in href.lower())
            next_js_root = soup.find("div", id="__next")
            
            if not pdf_links and next_js_root and not next_js_root.get_text(strip=True):
                logger.warning("Labour Ministry Next.js CSR block detected. Page requires JS hydration.")
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
                        content_type="application/pdf" if href.lower().endswith(".pdf") else "text/html"
                    ))
            logger.info("LabourCentralScraper fetch complete", doc_count=len(documents))
        except Exception as e:
            logger.error(f"Failed to fetch LabourCentralScraper", error=str(e))
            
        return documents

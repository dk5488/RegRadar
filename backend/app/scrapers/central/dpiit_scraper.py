"""
RegRadar — DPIIT Scraper
The Department for Promotion of Industry and Internal Trade (DPIIT) site 
is built on a Next.js Client-Side Rendering (CSR) architecture.
The raw HTML payload is empty (stub `<div id="__next">`) and hydrates purely via JS.
A pure GET-based scraper cannot natively parse its PDFs.
This scraper gracefully implements a block-detection to prevent pipeline crashes
and queues it for headless browser (Playwright) integration.
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)


class DPIITScraper(BaseScraper):
    source_name = "DPIIT — Department for Promotion of Industry"
    base_url = "https://dpiit.gov.in/whats-new/press-releases"
    fetch_frequency_hours = 24
    requires_pdf_extraction = True

    async def fetch(self) -> List[RawDocument]:
        documents = []
        try:
            response = await self.safe_get(self.base_url)
            soup = BeautifulSoup(response.text, "lxml")
            
            # Check if there are actual links or if we are hitting the Next.js empty root
            pdf_links = soup.find_all("a", href=lambda href: href and ".pdf" in href.lower())
            next_js_root = soup.find("div", id="__next")
            
            if not pdf_links and next_js_root and not next_js_root.get_text(strip=True):
                logger.warning("DPIIT Next.js CSR block detected. Page requires JS hydration.")
                return documents
                
            # Fallback parsing in case SSR gets enabled by DPIIT later
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
                    
            logger.info("DPIITScraper fetch complete", doc_count=len(documents))
        except Exception as e:
            logger.error(f"Failed to fetch DPIITScraper", error=str(e))
            
        return documents

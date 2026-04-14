"""
RegRadar — ESICScraper
Automated Scaffold
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)

class ESICScraper(BaseScraper):
    """
    Scraper for ESIC (Employees State Insurance Corporation) circulars and notifications.
    Filters for relevant compliance documents for businesses/MSMEs.
    """
    source_name = "ESIC — Employees State Insurance Corporation"
    base_url = "https://www.esic.gov.in/circulars"
    fetch_frequency_hours = 24
    requires_pdf_extraction = True

    async def fetch(self) -> List[RawDocument]:
        """
        Fetches and parses the list of ESIC circulars.
        """
        documents = []
        try:
            response = await self.safe_get(self.base_url)
            soup = BeautifulSoup(response.text, "lxml")
            
            for link in soup.find_all("a", href=True):
                href = link.get("href", "")
                title = link.get_text(strip=True)[:200]
                
                if not title or len(title) < 5:
                    continue

                if self.is_valuable_compliance_document(title, href):
                    full_url = self._resolve_url(href)
                    documents.append(RawDocument(
                        url=full_url,
                        title=title,
                        raw_text=title,
                        content_type="application/pdf" if href.lower().endswith(".pdf") else "text/html"
                    ))
            
            unique_docs = self._deduplicate_documents(documents)
            logger.info("ESICScraper fetch complete", doc_count=len(unique_docs))
            return unique_docs

        except Exception as e:
            logger.error(f"Failed to fetch ESICScraper", error=str(e))
            
        return documents

    def _resolve_url(self, href: str) -> str:
        """Helper to resolve relative URLs to full paths."""
        if href.startswith("http"):
            return href
        return f"https://www.esic.gov.in{href}"

    def _deduplicate_documents(self, documents: List[RawDocument]) -> List[RawDocument]:
        """Helper to ensure only unique URLs are returned."""
        seen_urls = set()
        unique = []
        for doc in documents:
            if doc.url not in seen_urls:
                unique.append(doc)
                seen_urls.add(doc.url)
        return unique

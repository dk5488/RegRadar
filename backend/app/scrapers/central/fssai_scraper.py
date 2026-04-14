"""
RegRadar — FSSAIScraper
Automated Scaffold
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)

class FSSAIScraper(BaseScraper):
    """
    Scraper for FSSAI (Food Safety and Standards Authority of India) advisories and orders.
    Essential for food-business MSMEs.
    """
    source_name = "FSSAI — Food Safety and Standards Authority"
    base_url = "https://www.fssai.gov.in/advisories-orders.php"
    fetch_frequency_hours = 24
    requires_pdf_extraction = True

    async def fetch(self) -> List[RawDocument]:
        """
        Fetches the latest FSSAI advisories and orders.
        """
        documents = []
        try:
            response = await self.safe_get(self.base_url)
            soup = BeautifulSoup(response.text, "lxml")
            
            # FSSAI often uses tables for advisories
            for link in soup.find_all("a", href=True):
                href = link.get("href", "")
                title = link.get_text(strip=True)[:200]
                
                # Check for PDF or advisory links
                is_doc = href.lower().endswith(".pdf") or "upload" in href.lower()
                
                if not title or len(title) < 5:
                    # Try to get title from row if text is empty
                    parent_row = link.find_parent("tr")
                    if parent_row:
                        title = parent_row.get_text(" ", strip=True)[:200]

                if is_doc and self.is_valuable_compliance_document(title, href):
                    full_url = self._resolve_url(href)
                    documents.append(RawDocument(
                        url=full_url,
                        title=title,
                        raw_text=title,
                        content_type="application/pdf" if href.lower().endswith(".pdf") else "text/html"
                    ))
            
            unique_docs = self._deduplicate_documents(documents)
            logger.info("FSSAIScraper fetch complete", doc_count=len(unique_docs))
            return unique_docs

        except Exception as e:
            logger.error(f"Failed to fetch FSSAIScraper", error=str(e))
            
        return documents

    def _resolve_url(self, href: str) -> str:
        """Resolves relative FSSAI URLs."""
        if href.startswith("http"):
            return href
        return f"https://www.fssai.gov.in/{href.lstrip('/')}"

    def _deduplicate_documents(self, documents: List[RawDocument]) -> List[RawDocument]:
        """Ensures unique documents based on URL."""
        seen_urls = set()
        unique = []
        for doc in documents:
            if doc.url not in seen_urls:
                unique.append(doc)
                seen_urls.add(doc.url)
        return unique

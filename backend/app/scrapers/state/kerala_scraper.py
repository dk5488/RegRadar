"""
RegRadar — KeralaScraper
Automated Scaffold for Kerala State Regulations
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)

class KeralaScraper(BaseScraper):
    source_name = "Kerala State Government"
    base_url = "https://lc.kerala.gov.in/"
    fetch_frequency_hours = 48
    requires_pdf_extraction = True

    SECONDARY_URLS = [
        "https://keralataxes.gov.in/circulars/"
    ]

    async def fetch(self) -> List[RawDocument]:
        documents = []
        try:
            # Fetch base url
            response = await self.safe_get(self.base_url)
            documents.extend(self._parse_page(response.text, self.base_url))
            
            # Fetch secondary urls
            for url in self.SECONDARY_URLS:
                sec_response = await self.safe_get(url)
                documents.extend(self._parse_page(sec_response.text, url))
                
            logger.info("KeralaScraper fetch complete", doc_count=len(documents))
        except Exception as e:
            logger.error(f"Failed to fetch KeralaScraper", error=str(e))
            
        return documents

    def _parse_page(self, html: str, source_url: str) -> List[RawDocument]:
        soup = BeautifulSoup(html, "lxml")
        parsed_docs = []
        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            title = link.get_text(strip=True)[:200]
            
            if not title or len(title) < 4:
                parent = link.parent
                if parent:
                    title = parent.get_text(strip=True)[:200]
                    
            if not title or len(title) < 4 or href.startswith("javascript:"):
                continue
            
            if self.is_valuable_compliance_document(title, href):
                from urllib.parse import urljoin
                full_url = urljoin(source_url, href)
                
                parsed_docs.append(RawDocument(
                    url=full_url,
                    title=title,
                    raw_text=title,
                    content_type="application/pdf" if href.lower().endswith(".pdf") else "text/html"
                ))
        return parsed_docs

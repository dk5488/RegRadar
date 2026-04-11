"""
RegRadar — BISScraper
Automated Scaffold
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)

class BISScraper(BaseScraper):
    source_name = "BIS — Bureau of Indian Standards"
    base_url = "https://www.bis.gov.in/others/notifications.htm"
    fetch_frequency_hours = 24
    requires_pdf_extraction = True

    async def fetch(self) -> List[RawDocument]:
        documents = []
        try:
            response = await self.safe_get(self.base_url)
            soup = BeautifulSoup(response.text, "lxml")
            
            for link in soup.find_all("a", href=True):
                href = link.get("href", "")
                title = link.get_text(strip=True)[:200]
                
                is_matched = (
                    href.lower().endswith(".pdf") or
                    any(kw in href.lower() or kw in title.lower() for kw in ["circular", "notification", "order", "rule", "amendment", "gazette"])
                )
                
                if is_matched and title:
                    full_url = href if href.startswith("http") else f"{self.base_url.rstrip('/')}/{href.lstrip('/')}"
                    documents.append(RawDocument(
                        url=full_url,
                        title=title,
                        raw_text=title,
                        content_type="application/pdf" if href.lower().endswith(".pdf") else "text/html"
                    ))
            logger.info("BISScraper fetch complete", doc_count=len(documents))
        except Exception as e:
            logger.error(f"Failed to fetch BISScraper", error=str(e))
            
        return documents

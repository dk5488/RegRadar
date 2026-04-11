"""
RegRadar — EPFOScraper
Automated Scaffold
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)

class EPFOScraper(BaseScraper):
    source_name = "EPFO — Employees Provident Fund Organisation"
    base_url = "https://www.epfindia.gov.in/site_en/Updates.php"
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
                
                if self.is_valuable_compliance_document(title, href):
                    full_url = href if href.startswith("http") else f"{self.base_url.rsplit('/', 1)[0]}/{href.lstrip('/')}"
                    documents.append(RawDocument(
                        url=full_url,
                        title=title,
                        raw_text=title,
                        content_type="application/pdf"
                    ))
            logger.info("EPFOScraper fetch complete", doc_count=len(documents))
        except Exception as e:
            logger.error(f"Failed to fetch EPFOScraper", error=str(e))
            
        return documents

"""
RegRadar — IncomeTaxScraper
Automated Scaffold
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)

class IncomeTaxScraper(BaseScraper):
    source_name = "Income Tax Department / CBDT"
    base_url = "https://incometaxindia.gov.in/notifications"
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
                
                if not title or len(title) < 5:
                    continue

                if self.is_valuable_compliance_document(title, href):
                    full_url = href if href.startswith("http") else f"https://incometaxindia.gov.in{href}"
                    documents.append(RawDocument(
                        url=full_url,
                        title=title,
                        raw_text=title,
                        content_type="application/pdf" if href.lower().endswith(".pdf") else "text/html"
                    ))
            
            # Remove duplicates
            seen_urls = set()
            unique_docs = []
            for doc in documents:
                if doc.url not in seen_urls:
                    unique_docs.append(doc)
                    seen_urls.add(doc.url)
            
            logger.info("IncomeTaxScraper fetch complete", doc_count=len(unique_docs))
            return unique_docs
        except Exception as e:
            logger.error(f"Failed to fetch IncomeTaxScraper", error=str(e))
            
        return documents

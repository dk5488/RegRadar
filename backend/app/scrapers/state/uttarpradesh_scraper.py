"""
RegRadar — UttarPradeshScraper
Automated Scaffold
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)

class UttarPradeshScraper(BaseScraper):
    source_name = "Uttar Pradesh Government"
    base_url = "https://uplabour.gov.in/"
    fetch_frequency_hours = 48
    requires_pdf_extraction = True

    async def fetch(self) -> List[RawDocument]:
        documents = []
        try:
            response = await self.safe_get(self.base_url)
            soup = BeautifulSoup(response.text, "lxml")
            
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
                    # Fix relative paths for UP Labour
                    if href.startswith("../"):
                        href = href.replace("../", "")
                        
                    full_url = href if href.startswith("http") else f"{self.base_url.rstrip('/')}/{href.lstrip('/')}"
                    documents.append(RawDocument(
                        url=full_url,
                        title=title,
                        raw_text=title,
                        content_type="application/pdf" if href.lower().endswith(".pdf") else "text/html"
                    ))
                    
            logger.info("UttarPradeshScraper fetch complete", doc_count=len(documents))
        except Exception as e:
            logger.error(f"Failed to fetch UttarPradeshScraper", error=str(e))
            
        return documents

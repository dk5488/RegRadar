"""
RegRadar — DGFTScraper
Automated Scaffold
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)

class DGFTScraper(BaseScraper):
    """
    Scraper for DGFT (Directorate General of Foreign Trade) notifications.
    Crucial for MSME exporters/importers.
    """
    source_name = "DGFT — Directorate General of Foreign Trade"
    base_url = "https://www.dgft.gov.in/CP/?opt=notification"
    fetch_frequency_hours = 24
    requires_pdf_extraction = True

    async def fetch(self) -> List[RawDocument]:
        """
        Fetches the latest DGFT notifications from the notification table.
        """
        documents = []
        try:
            response = await self.safe_get(self.base_url)
            soup = BeautifulSoup(response.text, "lxml")
            
            # DGFT notifications are typically in a table row <tr>
            # We look for rows and then find the download link and title within them.
            rows = soup.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 5:
                    continue
                
                # Column 4 (index 3) is usually the Subject/Title
                title = cols[3].get_text(strip=True)[:200]
                # Column 5 (index 4) is the Date
                notif_date = cols[4].get_text(strip=True)
                
                # The download link is in the last column
                download_link = row.find("a", href=True, title="Download")
                if not download_link:
                    # Fallback: look for any link with .pdf or Download in text
                    download_link = row.find("a", href=lambda h: h and (".pdf" in h.lower() or "download" in h.lower()))

                if download_link:
                    href = download_link["href"]
                    combined_title = f"{title} ({notif_date})"
                    
                    if self.is_valuable_compliance_document(combined_title, href):
                        documents.append(RawDocument(
                            url=href,
                            title=combined_title,
                            raw_text=combined_title,
                            content_type="application/pdf"
                        ))

            unique_docs = self._deduplicate_documents(documents)
            logger.info("DGFTScraper fetch complete", doc_count=len(unique_docs))
            return unique_docs

        except Exception as e:
            logger.error(f"Failed to fetch DGFTScraper", error=str(e))
            
        return documents

    def _deduplicate_documents(self, documents: List[RawDocument]) -> List[RawDocument]:
        """Ensures unique documents based on URL."""
        seen_urls = set()
        unique = []
        for doc in documents:
            if doc.url not in seen_urls:
                unique.append(doc)
                seen_urls.add(doc.url)
        return unique

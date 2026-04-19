"""
RegRadar — BIS Scraper
Bureau of Indian Standards — Notifications & Standards Circulars
Fetches regulatory notifications, amendments, and compliance orders
relevant to MSMEs from the BIS notifications page.
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

            logger.info("BISScraper fetch complete", doc_count=len(documents))
        except Exception as e:
            logger.error("Failed to fetch BISScraper", error=str(e))

        return documents

    def _resolve_url(self, href: str) -> str:
        """Resolve relative URLs against the BIS domain."""
        if href.startswith("http"):
            return href
        if href.startswith("/"):
            return f"https://www.bis.gov.in{href}"
        base = self.base_url.rsplit("/", 1)[0]
        return f"{base}/{href}"

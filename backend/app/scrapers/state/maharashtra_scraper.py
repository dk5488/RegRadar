"""
RegRadar — Maharashtra State Scraper
Section 4.2: State Government Sources — Maharashtra
"""

from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)


class MaharashtraScraper(BaseScraper):
    """
    Scraper for Maharashtra State Regulations.

    Primary URLs:
    - https://mahalabour.gov.in (Labour)
    - https://mahagst.gov.in (Commercial Taxes)
    - https://egazette.maharashtra.gov.in (State Gazette)
    """

    source_name = "Maharashtra State Government"
    base_url = "https://mahalabour.gov.in"
    fetch_frequency_hours = 72 
    requires_pdf_extraction = True
    requires_ocr_fallback = False

    SECONDARY_URLS = [
        "https://mahagst.gov.in",
        "https://egazette.maharashtra.gov.in"
    ]

    async def fetch(self) -> List[RawDocument]:
        """Fetch documents from Maharashtra portals."""
        documents = []

        try:
            response = await self.safe_get(self.base_url)
            docs = self._parse_maharashtra_portal(response.text, self.base_url)
            documents.extend(docs)
            logger.info("Maharashtra Labour page fetched", doc_count=len(docs))
        except Exception as e:
            logger.error("Failed to fetch Maharashtra Labour page", error=str(e))

        for url in self.SECONDARY_URLS:
            try:
                response = await self.safe_get(url)
                docs = self._parse_maharashtra_portal(response.text, url)
                documents.extend(docs)
                logger.info("Maharashtra secondary page fetched", url=url, doc_count=len(docs))
            except Exception as e:
                logger.error("Failed to fetch Maharashtra secondary page", url=url, error=str(e))

        seen_urls = set()
        unique_docs = []
        for doc in documents:
            if doc.url not in seen_urls:
                seen_urls.add(doc.url)
                unique_docs.append(doc)

        logger.info("Maharashtra fetch complete", total_unique=len(unique_docs))
        return unique_docs

    def _parse_maharashtra_portal(self, html: str, base_url: str) -> List[RawDocument]:
        """Parse Maharashtra state sub-portals."""
        soup = BeautifulSoup(html, "lxml")
        documents = []

        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            title = link.get_text(strip=True)[:200]

            is_matched = (
                href.lower().endswith(".pdf") or
                any(kw in href.lower() or kw in title.lower() for kw in ["circular", "gazette", "notification"])
            )

            if is_matched:
                full_url = self._resolve_url(href, base_url)
                documents.append(
                    RawDocument(
                        url=full_url,
                        title=title or "Maharashtra Notification",
                        raw_text=title or "",
                        content_type="application/pdf" if href.lower().endswith(".pdf") else "text/html"
                    )
                )

        return documents

    def _resolve_url(self, href: str, base: str) -> str:
        if href.startswith("http"):
            return href
        if href.startswith("/"):
            from urllib.parse import urlparse
            p = urlparse(base)
            return f"{p.scheme}://{p.netloc}{href}"
        return f"{base}/{href}"

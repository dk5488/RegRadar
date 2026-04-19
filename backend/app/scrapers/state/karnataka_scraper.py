"""
RegRadar — Karnataka State Scraper
Section 4.2: State Government Sources — Karnataka
"""

from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)


class KarnatakaScraper(BaseScraper):
    """
    Scraper for Karnataka State Regulations (Labour and Commercial Taxes).

    Primary URLs:
    - https://labour.karnataka.gov.in (Labour, Shops & Establishments, Min Wage)
    - https://ctax.kar.nic.in (Commercial Taxes, State GST)
    """

    source_name = "Karnataka State Government"
    base_url = "https://labour.karnataka.gov.in/48/department-notification/en"
    fetch_frequency_hours = 72  # State sites change less frequently (twice weekly)
    requires_pdf_extraction = True
    requires_ocr_fallback = False

    SECONDARY_URLS = [
        "https://labour.karnataka.gov.in/49/circulars/en",
        "https://gst.kar.nic.in/index.html"
    ]

    async def fetch(self) -> List[RawDocument]:
        """Fetch documents from both Labour and Commercial Taxes portals."""
        documents = []

        # 1. Fetch Labour Laws
        try:
            response = await self.safe_get(self.base_url)
            docs = self._parse_karnataka_portal(response.text, self.base_url)
            documents.extend(docs)
            logger.info("Karnataka Labour page fetched", doc_count=len(docs))
        except Exception as e:
            logger.error("Failed to fetch Karnataka Labour page", error=str(e))

        # 2. Fetch Commercial Taxes / SGST
        for url in self.SECONDARY_URLS:
            try:
                response = await self.safe_get(url)
                docs = self._parse_karnataka_portal(response.text, url)
                documents.extend(docs)
                logger.info("Karnataka Commercial Taxes page fetched", doc_count=len(docs))
            except Exception as e:
                logger.error("Failed to fetch Karnataka Commercial Taxes page", url=url, error=str(e))

        # De-duplicate
        seen_urls = set()
        unique_docs = []
        for doc in documents:
            if doc.url not in seen_urls:
                seen_urls.add(doc.url)
                unique_docs.append(doc)

        logger.info("Karnataka fetch complete", total_unique=len(unique_docs))
        return unique_docs

    def _parse_karnataka_portal(self, html: str, base_url: str) -> List[RawDocument]:
        """Parse Karnataka state sub-portals for PDF notifications."""
        soup = BeautifulSoup(html, "lxml")
        documents = []

        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            title = link.get_text(strip=True)[:200]

            if not title or len(title) < 5:
                continue

            if self.is_valuable_compliance_document(title, href):
                full_url = self._resolve_url(href, base_url)
                documents.append(
                    RawDocument(
                        url=full_url,
                        title=title,
                        raw_text=title,
                        content_type="application/pdf" if href.lower().endswith(".pdf") else "text/html"
                    )
                )

        return documents

    def _resolve_url(self, href: str, base: str) -> str:
        href = href.strip()
        if href.startswith("http"):
            return href
        if href.startswith("/"):
            from urllib.parse import urlparse
            p = urlparse(base)
            return f"{p.scheme}://{p.netloc}{href}"
        return f"{base.rstrip('/')}/{href}"

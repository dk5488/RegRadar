"""
RegRadar — MCA Scraper
Section 4, Source 1: Ministry of Corporate Affairs notifications.
PDFs are sometimes scanned — uses OCR fallback.
"""

from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)


class MCAScraper(BaseScraper):
    """
    Scraper for Ministry of Corporate Affairs (MCA).

    Primary URL: https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/notifications.html
    Secondary: https://www.mca.gov.in/MinistryV2/notification.html

    Section 4: "Site occasionally down. Use retry logic with 3 attempts
    and exponential backoff. PDFs are scanned in some older notifications —
    use OCR fallback when pdfplumber returns empty text."

    Change detection: "Hash the full list of PDF URLs on each fetch. New URLs
    = new notifications to process."
    """

    source_name = "Ministry of Corporate Affairs"
    base_url = "https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/notifications.html"
    fetch_frequency_hours = 24
    requires_pdf_extraction = True
    requires_ocr_fallback = True  # Section 4: scanned PDFs in older notifications

    SECONDARY_URLS = [
        "https://www.mca.gov.in/MinistryV2/notification.html",
    ]

    async def fetch(self) -> List[RawDocument]:
        """
        Fetch new notifications from MCA.
        Section 4: "Page lists notifications as links to PDFs."
        """
        documents = []

        # Fetch primary URL
        try:
            response = await self.safe_get(self.base_url)
            docs = self._parse_notification_page(response.text, self.base_url)
            documents.extend(docs)
            logger.info("MCA primary page fetched", doc_count=len(docs))
        except Exception as e:
            logger.error("Failed to fetch MCA primary page", error=str(e))

        # Fetch secondary URLs
        for url in self.SECONDARY_URLS:
            try:
                response = await self.safe_get(url)
                docs = self._parse_notification_page(response.text, url)
                documents.extend(docs)
                logger.info("MCA secondary page fetched", url=url, doc_count=len(docs))
            except Exception as e:
                logger.warning("Failed to fetch MCA secondary page", url=url, error=str(e))

        # De-duplicate by URL
        seen_urls = set()
        unique_docs = []
        for doc in documents:
            if doc.url not in seen_urls:
                seen_urls.add(doc.url)
                unique_docs.append(doc)

        logger.info("MCA fetch complete", total_unique=len(unique_docs))
        return unique_docs

    def _parse_notification_page(self, html: str, base_url: str) -> List[RawDocument]:
        """
        Parse MCA notification listing page.
        Multiple CSS fallback paths for resilience (Section 13, Risk 1).
        """
        soup = BeautifulSoup(html, "lxml")
        documents = []

        # Strategy 1: Look for notification tables
        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                link = row.find("a", href=True)
                if not link:
                    continue

                href = link.get("href", "")
                title = link.get_text(strip=True)

                if self._is_notification_link(href):
                    full_url = self._resolve_url(href, base_url)
                    documents.append(
                        RawDocument(
                            url=full_url,
                            title=title[:200] if title else "MCA Notification",
                            raw_text=title or "",
                            content_type="application/pdf" if href.endswith(".pdf") else "text/html",
                        )
                    )

        # Strategy 2: Look for notification divs/lists
        if not documents:
            for container in soup.find_all(["div", "ul", "ol"],
                                           class_=lambda c: c and any(
                                               kw in str(c).lower()
                                               for kw in ["notification", "circular", "list", "content"]
                                           )):
                for link in container.find_all("a", href=True):
                    href = link.get("href", "")
                    if self._is_notification_link(href):
                        full_url = self._resolve_url(href, base_url)
                        documents.append(
                            RawDocument(
                                url=full_url,
                                title=link.get_text(strip=True)[:200],
                                raw_text=link.get_text(strip=True),
                            )
                        )

        # Strategy 3: Fallback — grab all PDF links on the page
        if not documents:
            for link in soup.find_all("a", href=True):
                href = link.get("href", "")
                if href.lower().endswith(".pdf"):
                    full_url = self._resolve_url(href, base_url)
                    documents.append(
                        RawDocument(
                            url=full_url,
                            title=link.get_text(strip=True)[:200] or "MCA PDF",
                            raw_text=link.get_text(strip=True),
                            content_type="application/pdf",
                        )
                    )

        return documents

    def _is_notification_link(self, href: str) -> bool:
        """Check if a URL looks like a notification/circular link."""
        href_lower = href.lower()
        return any(kw in href_lower for kw in [
            ".pdf", "notification", "circular", "order", "rule",
            "amendment", "gazette", "act",
        ])

    def _resolve_url(self, href: str, base_url: str) -> str:
        """Resolve relative URLs to absolute."""
        if href.startswith("http"):
            return href
        if href.startswith("/"):
            from urllib.parse import urlparse
            parsed = urlparse(base_url)
            return f"{parsed.scheme}://{parsed.netloc}{href}"
        base = base_url.rsplit("/", 1)[0]
        return f"{base}/{href}"

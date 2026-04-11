"""
RegRadar — CBIC/GST Scraper
Section 4, Source 2: Scrapes CBIC notifications for GST rule changes.
Most time-sensitive source — fetches twice daily.
"""

from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)


class CBICScraper(BaseScraper):
    """
    Scraper for CBIC (Central Board of Indirect Customs & Customs) / GST Council.

    Primary URL: https://www.cbic.gov.in/htdocs-cbec/gst/index.htm
    Secondary: https://gstcouncil.gov.in/press-release

    Section 4: "Track the highest notification number seen per notification
    type per year. Any new number triggers fetch and processing."
    """

    source_name = "CBIC / GST Council"
    base_url = "https://gstcouncil.gov.in/press-release"
    fetch_frequency_hours = 12
    requires_pdf_extraction = True
    requires_ocr_fallback = False

    # Notification type pages to check
    NOTIFICATION_URLS = [
        "https://gstcouncil.gov.in/gst-circulars",
        "https://gstcouncil.gov.in/gst-notifications"
    ]

    async def fetch(self) -> List[RawDocument]:
        """
        Fetch new GST notifications from CBIC.
        Scrapes the main index page and notification listing pages.
        """
        documents = []

        # Fetch main index page
        try:
            response = await self.safe_get(self.base_url)
            docs_from_index = self._parse_notification_index(response.text, self.base_url)
            documents.extend(docs_from_index)
        except Exception as e:
            logger.error("Failed to fetch CBIC index", error=str(e))

        # Fetch each notification type page
        for url in self.NOTIFICATION_URLS:
            try:
                response = await self.safe_get(url)
                docs = self._parse_notification_page(response.text, url)
                documents.extend(docs)
            except Exception as e:
                logger.warning("Failed to fetch CBIC notification page", url=url, error=str(e))
                continue

        # Fetch GST Council press releases
        try:
            response = await self.safe_get("https://gstcouncil.gov.in/press-release")
            press_docs = self._parse_gst_council_press(response.text)
            documents.extend(press_docs)
        except Exception as e:
            logger.warning("Failed to fetch GST Council press releases", error=str(e))

        logger.info("CBIC fetch complete", total_documents=len(documents))
        return documents

    def _parse_notification_index(self, html: str, base_url: str) -> List[RawDocument]:
        """Parse the CBIC main GST index page for notification links."""
        soup = BeautifulSoup(html, "lxml")
        documents = []

        # CBIC typically lists notifications in table rows or anchors
        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            text = link.get_text(strip=True)

            # Filter for notification PDFs and pages
            if any(kw in href.lower() for kw in [".pdf", "notification", "circular", "order"]):
                full_url = self._resolve_url(href, base_url)
                if full_url and text:
                    documents.append(
                        RawDocument(
                            url=full_url,
                            title=text[:200],
                            raw_text=text,
                            content_type="application/pdf" if href.endswith(".pdf") else "text/html",
                        )
                    )

        return documents

    def _parse_notification_page(self, html: str, base_url: str) -> List[RawDocument]:
        """Parse a specific CBIC notification type page."""
        soup = BeautifulSoup(html, "lxml")
        documents = []

        # Look for tables with notification listings
        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) < 2:
                    continue

                link = row.find("a", href=True)
                if not link:
                    continue

                href = link.get("href", "")
                title = link.get_text(strip=True) or cells[0].get_text(strip=True)

                if href:
                    full_url = self._resolve_url(href, base_url)
                    documents.append(
                        RawDocument(
                            url=full_url,
                            title=title[:200],
                            raw_text=title,
                        )
                    )

        # Also check for links outside tables
        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            if href.endswith(".pdf") and href not in [d.url for d in documents]:
                full_url = self._resolve_url(href, base_url)
                documents.append(
                    RawDocument(
                        url=full_url,
                        title=link.get_text(strip=True)[:200],
                        raw_text=link.get_text(strip=True),
                        content_type="application/pdf",
                    )
                )

        return documents

    def _parse_gst_council_press(self, html: str) -> List[RawDocument]:
        """Parse GST Council press releases page."""
        soup = BeautifulSoup(html, "lxml")
        documents = []

        for article in soup.find_all("a", href=True):
            href = article.get("href", "")
            title = article.get_text(strip=True)[:200]
            
            if href.lower().endswith(".pdf") or "press" in href.lower():
                if not self.is_valuable_compliance_document(title, href):
                    continue
                full_url = self._resolve_url(href, "https://gstcouncil.gov.in")
                documents.append(
                    RawDocument(
                        url=full_url,
                        title=title or href.split("/")[-1],
                        raw_text=title or href.split("/")[-1],
                        content_type="application/pdf" if href.endswith(".pdf") else "text/html",
                    )
                )

        # Fallback: just get all PDF links
        if not documents:
            for link in soup.find_all("a", href=True):
                href = link.get("href", "")
                if href.lower().endswith(".pdf"):
                    title_text = link.get_text(strip=True)[:200] or href.split("/")[-1]
                    if self.is_valuable_compliance_document(title_text, href):
                        documents.append(
                            RawDocument(
                                url=self._resolve_url(href, "https://gstcouncil.gov.in"),
                                title=title_text,
                                raw_text=link.get_text(strip=True) or href.split("/")[-1],
                                content_type="application/pdf",
                            )
                        )

        return documents

    def _resolve_url(self, href: str, base_url: str) -> str:
        """Resolve relative URLs to absolute."""
        if href.startswith("http"):
            return href
        if href.startswith("/"):
            from urllib.parse import urlparse
            parsed = urlparse(base_url)
            return f"{parsed.scheme}://{parsed.netloc}{href}"
        # Relative URL
        base = base_url.rsplit("/", 1)[0]
        return f"{base}/{href}"

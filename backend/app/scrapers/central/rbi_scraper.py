"""
RegRadar — RBI Scraper
Section 4, Source 3: Reserve Bank of India notifications via RSS feed.
RSS is more reliable than scraping — use as primary method.
"""

from typing import List
from datetime import datetime, timezone
import feedparser
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)


class RBIScraper(BaseScraper):
    """
    Scraper for Reserve Bank of India (RBI).

    Primary: RSS feed at https://www.rbi.org.in/rss/RBINotifications.xml
    Fallback: Scrape https://www.rbi.org.in/Scripts/NotificationUser.aspx

    Section 4: "RSS feed first. Fall back to scraper if RSS fails."
    "RBI RSS feed is generally reliable. Occasional encoding issues in
    Hindi content — use UTF-8 encoding explicitly."
    """

    source_name = "Reserve Bank of India"
    base_url = "https://www.rbi.org.in/Scripts/NotificationUser.aspx"
    fetch_frequency_hours = 24
    requires_pdf_extraction = True
    requires_ocr_fallback = False

    RSS_URL = "https://www.rbi.org.in/rss/RBINotifications.xml"
    PRESS_URL = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx"

    async def fetch(self) -> List[RawDocument]:
        """Fetch via RSS first, fall back to HTML scraping."""
        documents = []

        # Try RSS feed first (preferred)
        try:
            rss_docs = await self._fetch_rss()
            documents.extend(rss_docs)
            logger.info("RBI RSS feed fetched", doc_count=len(rss_docs))
        except Exception as e:
            logger.warning("RBI RSS feed failed, falling back to scraper", error=str(e))
            # Fallback to HTML scraping
            try:
                html_docs = await self._fetch_html()
                documents.extend(html_docs)
            except Exception as e2:
                logger.error("RBI HTML fallback also failed", error=str(e2))

        # Also check press releases
        try:
            press_docs = await self._fetch_press_releases()
            documents.extend(press_docs)
        except Exception as e:
            logger.warning("RBI press releases fetch failed", error=str(e))

        return documents

    async def _fetch_rss(self) -> List[RawDocument]:
        """Parse the RBI RSS feed for notifications."""
        response = await self.safe_get(self.RSS_URL)

        # Explicit UTF-8 handling (Section 4: encoding issues)
        content = response.text.encode("utf-8", errors="replace").decode("utf-8")
        feed = feedparser.parse(content)

        documents = []
        for entry in feed.entries:
            title = entry.get("title", "RBI Notification")
            link = entry.get("link", "")
            summary = entry.get("summary", "")
            published = entry.get("published", "")

            if link:
                documents.append(
                    RawDocument(
                        url=link,
                        title=title[:200],
                        raw_text=f"{title}\n\n{summary}",
                        metadata={"published": published},
                    )
                )

        return documents

    async def _fetch_html(self) -> List[RawDocument]:
        """Fallback: scrape the notification listing page."""
        response = await self.safe_get(self.base_url)
        soup = BeautifulSoup(response.text, "lxml")
        documents = []

        # RBI lists notifications in a table
        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                link = row.find("a", href=True)
                if link:
                    href = link.get("href", "")
                    if href and ("notification" in href.lower() or href.endswith(".pdf")):
                        full_url = self._resolve_url(href)
                        documents.append(
                            RawDocument(
                                url=full_url,
                                title=link.get_text(strip=True)[:200],
                                raw_text=link.get_text(strip=True),
                            )
                        )

        return documents

    async def _fetch_press_releases(self) -> List[RawDocument]:
        """Fetch RBI press releases."""
        response = await self.safe_get(self.PRESS_URL)
        soup = BeautifulSoup(response.text, "lxml")
        documents = []

        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            text = link.get_text(strip=True)
            if text and ("press" in href.lower() or href.endswith(".pdf")):
                full_url = self._resolve_url(href)
                documents.append(
                    RawDocument(
                        url=full_url,
                        title=text[:200],
                        raw_text=text,
                    )
                )

        return documents

    def _resolve_url(self, href: str) -> str:
        """Resolve relative URLs."""
        if href.startswith("http"):
            return href
        return f"https://www.rbi.org.in{href}" if href.startswith("/") else f"https://www.rbi.org.in/{href}"

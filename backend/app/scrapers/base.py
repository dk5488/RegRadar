"""
RegRadar — Base Scraper
Abstract base class for all regulatory source scrapers.
Implements retry logic, anti-blocking measures, and the fetch pipeline
as specified in Section 8 of the project context document.
"""

import abc
import hashlib
import random
import time
import asyncio
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timezone

from curl_cffi.requests import AsyncSession
from curl_cffi import requests as cffi_requests
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.logging import get_logger

logger = get_logger(__name__)

# ── User-Agent pool (Section 8: 10 realistic browser strings) ─────────
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]


@dataclass
class RawDocument:
    """A single fetched document from a regulatory source."""
    url: str
    title: Optional[str] = None
    raw_content: bytes = b""
    raw_text: Optional[str] = None
    content_type: str = "text/html"  # or "application/pdf"
    fetched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict = field(default_factory=dict)


class BaseScraper(abc.ABC):
    """
    Abstract base class for all RegRadar scrapers.
    Subclasses must implement `fetch()` and optionally override `extract_text()`.
    """

    source_id: str = ""
    source_name: str = ""
    base_url: str = ""
    fetch_frequency_hours: int = 24
    requires_pdf_extraction: bool = False
    requires_ocr_fallback: bool = False
    request_timeout: int = 30  # seconds

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        self._session: Optional[AsyncSession] = None

    async def get_client(self) -> AsyncSession:
        """Create or return an AsyncSession with anti-blocking headers and TLS impersonation."""
        if self._session is None or self._session._closed:
            proxies = {"http": self.proxy_url, "https": self.proxy_url} if self.proxy_url else None
            self._session = AsyncSession(
                timeout=self.request_timeout,
                proxies=proxies,
                impersonate="chrome",
                headers=self._get_headers(),
                verify=False
            )
        return self._session

    def _get_headers(self) -> dict:
        """Random User-Agent + Indian locale headers (Section 8)."""
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-IN,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=4, max=30))
    async def safe_get(self, url: str) -> "cffi_requests.Response":
        """
        GET request with retry logic and random delay.
        """
        # Random delay between requests
        delay = random.uniform(0.1, 0.5)
        logger.debug("Waiting before request", delay_seconds=round(delay, 2))
        await asyncio.sleep(delay)

        client = await self.get_client()
        response = await client.get(url, headers=self._get_headers())
        response.raise_for_status()

        # Verify we got actual content (not a maintenance page)
        if len(response.text) < 200:
            logger.warning("Suspiciously short response", url=url, length=len(response.text))

        return response

    @abc.abstractmethod
    async def fetch(self) -> List[RawDocument]:
        """
        Fetch all new/changed documents from the source.
        Must return a list of RawDocument objects.
        """
        ...

    def compute_hash(self, text: str) -> str:
        """
        SHA-256 hash of normalised text content.
        Section 8: lowercase, strip whitespace, remove page numbers/headers.
        """
        normalised = text.lower().strip()
        # Remove common page artifacts
        import re
        normalised = re.sub(r"page\s*\d+\s*(of\s*\d+)?", "", normalised)
        normalised = re.sub(r"\s+", " ", normalised)
        return hashlib.sha256(normalised.encode("utf-8")).hexdigest()

    async def close(self):
        """Close the HTTP client."""
        if self._session and not self._session._closed:
            self._session.close()

    def __repr__(self):
        return f"<{self.__class__.__name__} source='{self.source_name}'>"

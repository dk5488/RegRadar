"""
RegRadar — IRDAI Scraper
Insurance Regulatory and Development Authority of India
Fetches circulars, notifications, and guidelines relevant to
insurance compliance for MSMEs.
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)


class IRDAIScraper(BaseScraper):
    source_name = "IRDAI — Insurance Regulatory"
    base_url = "https://irdai.gov.in/circulars"
    fetch_frequency_hours = 24
    requires_pdf_extraction = True

    SECONDARY_URLS = [
        "https://irdai.gov.in/notifications",
    ]

    async def fetch(self) -> List[RawDocument]:
        documents = []
        seen_urls = set()

        all_urls = [self.base_url] + self.SECONDARY_URLS
        for page_url in all_urls:
            try:
                response = await self.safe_get(page_url)
                docs = self._parse_page(response.text, page_url)
                for doc in docs:
                    if doc.url not in seen_urls:
                        seen_urls.add(doc.url)
                        documents.append(doc)
                logger.info("IRDAI page fetched", url=page_url, doc_count=len(docs))
            except Exception as e:
                logger.warning("Failed to fetch IRDAI page", url=page_url, error=str(e))

        logger.info("IRDAIScraper fetch complete", total=len(documents))
        return documents

    def _parse_page(self, html: str, base_url: str) -> List[RawDocument]:
        soup = BeautifulSoup(html, "lxml")
        documents = []

        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            title = link.get_text(strip=True)[:200]

            if not title or len(title) < 5:
                continue

            # IRDAI uses Liferay CMS — docs live under /documents/ paths
            is_doc_link = (
                ".pdf" in href.lower() or
                "/documents/" in href
            )

            if is_doc_link and self.is_valuable_compliance_document(title, href):
                full_url = self._resolve_url(href)
                documents.append(RawDocument(
                    url=full_url,
                    title=title,
                    raw_text=title,
                    content_type="application/pdf" if ".pdf" in href.lower() else "text/html",
                ))

        return documents

    def _resolve_url(self, href: str) -> str:
        if href.startswith("http"):
            return href
        if href.startswith("/"):
            return f"https://irdai.gov.in{href}"
        return f"https://irdai.gov.in/{href}"

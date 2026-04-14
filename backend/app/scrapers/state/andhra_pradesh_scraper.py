"""
RegRadar — Andhra Pradesh State Scraper
Section 4.2: State Government Sources — Andhra Pradesh
"""

import re
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)


class AndhraPradeshScraper(BaseScraper):
    """
    Scraper for Andhra Pradesh State Regulations.

    Primary URLs:
    - https://apegazette.cgg.gov.in (Official Gazette - covers all depts)
    - https://apct.gov.in/gst-info (Commercial Taxes)
    - https://www.apindustries.gov.in (Industries & MSME)
    """

    source_name = "Andhra Pradesh State Government"
    base_url = "https://apegazette.cgg.gov.in"
    fetch_frequency_hours = 72
    requires_pdf_extraction = True
    requires_ocr_fallback = False

    SECONDARY_URLS = [
        "https://apct.gov.in/gst-info",
        "https://www.apindustries.gov.in/APIndus/Default.aspx"
    ]

    async def fetch(self) -> List[RawDocument]:
        """Fetch documents from Andhra Pradesh portals."""
        documents = []

        # 1. Fetch from AP Gazette
        try:
            response = await self.safe_get(self.base_url)
            gazette_docs = self._parse_gazette(response.text)
            documents.extend(gazette_docs)
            logger.info("AP Gazette page fetched", doc_count=len(gazette_docs))
        except Exception as e:
            logger.error("Failed to fetch AP Gazette page", error=str(e))

        # 2. Fetch from Secondary URLs
        for url in self.SECONDARY_URLS:
            try:
                response = await self.safe_get(url)
                docs = self._parse_generic_portal(response.text, url)
                documents.extend(docs)
                logger.info("AP secondary page fetched", url=url, doc_count=len(docs))
            except Exception as e:
                logger.error("Failed to fetch AP secondary page", url=url, error=str(e))

        # De-duplicate
        seen_urls = set()
        unique_docs = []
        for doc in documents:
            if doc.url not in seen_urls:
                seen_urls.add(doc.url)
                unique_docs.append(doc)

        logger.info("Andhra Pradesh fetch complete", total_unique=len(unique_docs))
        return unique_docs

    def _parse_gazette(self, html: str) -> List[RawDocument]:
        """Parse AP Gazette portal for recent notifications."""
        soup = BeautifulSoup(html, "lxml")
        documents = []
        
        # The gazette site has tables for "Recent Extraordinary Gazettes" and "Recent Weekly Gazettes"
        for table in soup.find_all("table"):
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if not cols:
                    continue
                
                # Check for <a> tags in each row
                links = row.find_all("a", href=True)
                for link in links:
                    href = link.get("href", "")
                    onclick = link.get("onclick", "")
                    
                    # Extract title from row text if possible, otherwise link text
                    row_text = row.get_text(separator=" ", strip=True)
                    title = row_text[:400] if row_text else link.get_text(strip=True)
                    
                    # Additional filtering for individual-specific or irrelevant Gazette notices
                    noise_patterns = [
                        r"\bSri\b", r"\bSmt\b", r"\bKumari\b", r"\bDr\b",
                        r"unauthorised absence", r"discharged", r"disciplinary action",
                        r"dismissal", r"pension", r"family pension", r"compassionate appointment",
                        r"transfer and posting", r"leave of absence", r"show cause notice"
                    ]
                    if any(re.search(pattern, title, re.IGNORECASE) for pattern in noise_patterns):
                        continue

                    actual_url = None
                    if "openDocument" in onclick:
                        # Extract the JWT-like payload from openDocument('...')
                        match = re.search(r"openDocument\('([^']+)'\)", onclick)
                        if match:
                            payload_encoded = match.group(1)
                            actual_url = self._decode_gazette_url(payload_encoded)
                    
                    if not actual_url and self.is_valuable_compliance_document(title, href):
                         actual_url = self._resolve_url(href, self.base_url)
                    
                    if actual_url and self.is_valuable_compliance_document(title, actual_url):
                        documents.append(
                            RawDocument(
                                url=actual_url,
                                title=title,
                                raw_text=title,
                                content_type="application/pdf" if actual_url.lower().endswith(".pdf") else "text/html"
                            )
                        )
        return documents

    def _decode_gazette_url(self, token: str) -> str:
        """Decodes the JWT-like token used by AP Gazette to find the PDF path."""
        try:
            # JWT is header.payload.signature
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            payload_b64 = parts[1]
            # Add padding if necessary
            missing_padding = len(payload_b64) % 4
            if missing_padding:
                payload_b64 += '=' * (4 - missing_padding)
            
            import base64
            import json
            payload_json = base64.b64decode(payload_b64).decode('utf-8')
            payload = json.loads(payload_json)
            
            # The 'sub' field contains the relative path
            path = payload.get('sub')
            if path:
                return self._resolve_url(path, self.base_url)
        except Exception as e:
            logger.debug("Failed to decode gazette token", error=str(e))
        return None

    def _parse_generic_portal(self, html: str, base_url: str) -> List[RawDocument]:
        """Generic parser for state portals."""
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
                        content_type="application/pdf" if href.lower().endswith(".pdf") or "download" in href.lower() else "text/html"
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
        # Handle relative paths
        if "/" not in href and "." in href:
             return f"{base.rstrip('/')}/{href}"
        
        from urllib.parse import urljoin
        return urljoin(base, href)

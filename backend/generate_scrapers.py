import os
from pathlib import Path

CENTRAL_DIR = Path("app/scrapers/central")
STATE_DIR = Path("app/scrapers/state")

CENTRAL_SCRAPERS = [
    ("sebi_scraper", "SEBIScraper", "SEBI — Securities and Exchange Board of India", "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doListingCircular=yes"),
    ("epfo_scraper", "EPFOScraper", "EPFO — Employees Provident Fund Organisation", "https://www.epfindia.gov.in/site_en/Circulars.php"),
    ("esic_scraper", "ESICScraper", "ESIC — Employees State Insurance Corporation", "https://www.esic.gov.in/circular"),
    ("labour_central_scraper", "LabourCentralScraper", "Ministry of Labour and Employment", "https://labour.gov.in/notifications"),
    ("dpiit_scraper", "DPIITScraper", "DPIIT — Department for Promotion of Industry", "https://dpiit.gov.in/whats-new/press-releases"),
    ("incometax_scraper", "IncomeTaxScraper", "Income Tax Department / CBDT", "https://www.incometaxindia.gov.in/Pages/communications/notifications.aspx"),
    ("gazette_scraper", "GazetteScraper", "Gazette of India", "https://egazette.gov.in"),
    ("dgft_scraper", "DGFTScraper", "DGFT — Directorate General of Foreign Trade", "https://www.dgft.gov.in/CP/?opt=notification"),
    ("fssai_scraper", "FSSAIScraper", "FSSAI — Food Safety and Standards Authority", "https://fssai.gov.in/home/fss-legislation/fssai-order-circular.html"),
    ("bis_scraper", "BISScraper", "BIS — Bureau of Indian Standards", "https://www.bis.gov.in/others/notifications.htm"),
    ("irdai_scraper", "IRDAIScraper", "IRDAI — Insurance Regulatory", "https://irdai.gov.in/web/guest/home/-/asset_publisher/oPq5fjJ0CKwz/circulars"),
]

STATE_SCRAPERS = [
    ("tamilnadu_scraper", "TamilNaduScraper", "Tamil Nadu State Government", "https://labour.tn.gov.in/"),
    ("delhi_scraper", "DelhiScraper", "Delhi NCT Government", "https://labour.delhi.gov.in/"),
    ("gujarat_scraper", "GujaratScraper", "Gujarat State Government", "https://labour.gujarat.gov.in/"),
]

TEMPLATE = '''"""
RegRadar — {class_name}
Automated Scaffold
"""
from typing import List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper, RawDocument
from app.core.logging import get_logger

logger = get_logger(__name__)

class {class_name}(BaseScraper):
    source_name = "{source_name}"
    base_url = "{base_url}"
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
                
                is_matched = (
                    href.lower().endswith(".pdf") or
                    any(kw in href.lower() or kw in title.lower() for kw in ["circular", "notification", "order", "rule", "amendment", "gazette"])
                )
                
                if is_matched and title:
                    full_url = href if href.startswith("http") else f"{{self.base_url.rstrip('/')}}/{{href.lstrip('/')}}"
                    documents.append(RawDocument(
                        url=full_url,
                        title=title,
                        raw_text=title,
                        content_type="application/pdf" if href.lower().endswith(".pdf") else "text/html"
                    ))
            logger.info("{class_name} fetch complete", doc_count=len(documents))
        except Exception as e:
            logger.error(f"Failed to fetch {class_name}", error=str(e))
            
        return documents
'''

if __name__ == "__main__":
    registry_imports = []
    registry_mappings = []

    # Central
    for module, cls, name, url in CENTRAL_SCRAPERS:
        path = CENTRAL_DIR / f"{module}.py"
        path.write_text(TEMPLATE.format(class_name=cls, source_name=name, base_url=url), encoding="utf-8")
        registry_imports.append(f"        from app.scrapers.central.{module} import {cls}")
        registry_mappings.append(f"        SCRAPER_REGISTRY['{module}'] = {cls}")
        
    # State
    for module, cls, name, url in STATE_SCRAPERS:
        path = STATE_DIR / f"{module}.py"
        path.write_text(TEMPLATE.format(class_name=cls, source_name=name, base_url=url), encoding="utf-8")
        registry_imports.append(f"        from app.scrapers.state.{module} import {cls}")
        registry_mappings.append(f"        SCRAPER_REGISTRY['{module}'] = {cls}")

    print("All scrapers generated successfully.")

    # Write a quick text out we can paste into __init__.py manually if needed
    with open("registry_injection.txt", "w") as f:
        f.write("\n".join(registry_imports))
        f.write("\n\n")
        f.write("\n".join(registry_mappings))

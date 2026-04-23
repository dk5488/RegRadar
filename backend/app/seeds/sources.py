"""
RegRadar — Seed Data: Regulatory Sources
Pre-populates the sources table with all government sources from Section 4.
Run: python -m app.seeds.sources
"""

REGULATORY_SOURCES = [
    # ── Central Government Sources ──────────────────────────────────
    {
        "name": "Ministry of Corporate Affairs",
        "short_code": "MCA",
        "base_url": "https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/notifications.html",
        "secondary_urls": [
            "https://www.mca.gov.in/MinistryV2/notification.html"
        ],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "mca_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": True,
    },
    {
        "name": "CBIC / GST Council",
        "short_code": "CBIC",
        "base_url": "https://www.cbic.gov.in/htdocs-cbec/gst/index.htm",
        "secondary_urls": [
            "https://gstcouncil.gov.in/press-release"
        ],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 12,
        "scraper_module_name": "cbic_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "Reserve Bank of India",
        "short_code": "RBI",
        "base_url": "https://www.rbi.org.in/Scripts/NotificationUser.aspx",
        "secondary_urls": [
            "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx",
            "https://www.rbi.org.in/rss/RBINotifications.xml",
        ],
        "fetch_method": "rss",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "rbi_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "SEBI",
        "short_code": "SEBI",
        "base_url": "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doListingCircular=yes",
        "secondary_urls": [
            "https://www.sebi.gov.in/rss.html"
        ],
        "fetch_method": "rss",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "sebi_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "EPFO",
        "short_code": "EPFO",
        "base_url": "https://www.epfindia.gov.in/site_en/Circulars.php",
        "secondary_urls": [],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "epfo_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": True,
    },
    {
        "name": "ESIC",
        "short_code": "ESIC",
        "base_url": "https://www.esic.gov.in/circular",
        "secondary_urls": [],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "esic_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "Ministry of Labour and Employment",
        "short_code": "MOLE",
        "base_url": "https://labour.gov.in/notifications",
        "secondary_urls": [
            "https://labour.gov.in/whats-new"
        ],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "labour_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "DPIIT",
        "short_code": "DPIIT",
        "base_url": "https://dpiit.gov.in/whats-new/press-releases",
        "secondary_urls": [
            "https://dpiit.gov.in/notifications"
        ],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "dpiit_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "Income Tax Department / CBDT",
        "short_code": "CBDT",
        "base_url": "https://www.incometaxindia.gov.in/Pages/communications/notifications.aspx",
        "secondary_urls": [
            "https://www.incometaxindia.gov.in/Pages/communications/circulars.aspx"
        ],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "cbdt_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "Gazette of India",
        "short_code": "GAZETTE",
        "base_url": "https://egazette.gov.in",
        "secondary_urls": [],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "gazette_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": True,
    },
    {
        "name": "DGFT",
        "short_code": "DGFT",
        "base_url": "https://www.dgft.gov.in/CP/",
        "secondary_urls": [
            "https://www.dgft.gov.in/CP/?opt=notification",
            "https://www.dgft.gov.in/CP/?opt=trade-notices",
        ],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "dgft_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "FSSAI",
        "short_code": "FSSAI",
        "base_url": "https://fssai.gov.in/home/fss-legislation/fssai-order-circular.html",
        "secondary_urls": [
            "https://fssai.gov.in/home/fss-legislation/gazette-notification.html"
        ],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "fssai_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "BIS",
        "short_code": "BIS",
        "base_url": "https://www.bis.gov.in/others/notifications.htm",
        "secondary_urls": [
            "https://www.bis.gov.in/index.php/others/press-release/"
        ],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "bis_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "IRDAI",
        "short_code": "IRDAI",
        "base_url": "https://irdai.gov.in/web/guest/home/-/asset_publisher/oPq5fjJ0CKwz/circulars",
        "secondary_urls": [],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "irdai_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "MSME Ministry",
        "short_code": "MSME",
        "base_url": "https://msme.gov.in/whats-new",
        "secondary_urls": [
            "https://udyamregistration.gov.in"
        ],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 24,
        "scraper_module_name": "msme_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },

    # ── State Government Sources (MVP: Karnataka & Maharashtra) ─────
    {
        "name": "Karnataka Labour Department",
        "short_code": "KA_LABOUR",
        "base_url": "https://labour.karnataka.gov.in",
        "secondary_urls": [],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 84,  # twice weekly
        "scraper_module_name": "karnataka_labour_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "Karnataka Commercial Taxes",
        "short_code": "KA_GST",
        "base_url": "https://ctax.kar.nic.in",
        "secondary_urls": [],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 84,
        "scraper_module_name": "karnataka_gst_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "Maharashtra Labour Department",
        "short_code": "MH_LABOUR",
        "base_url": "https://mahalabour.gov.in",
        "secondary_urls": [],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 84,
        "scraper_module_name": "maharashtra_labour_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "Maharashtra GST",
        "short_code": "MH_GST",
        "base_url": "https://mahagst.gov.in",
        "secondary_urls": [
            "https://egazette.maharashtra.gov.in"
        ],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 84,
        "scraper_module_name": "maharashtra_gst_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
    {
        "name": "Andhra Pradesh State Government",
        "short_code": "AP_GOVT",
        "base_url": "https://apegazette.cgg.gov.in",
        "secondary_urls": [
            "https://apct.gov.in/gst-info",
            "https://www.apindustries.gov.in/APIndus/Default.aspx"
        ],
        "fetch_method": "http_scraper",
        "fetch_frequency_hours": 72,
        "scraper_module_name": "andhra_pradesh_scraper",
        "requires_pdf_extraction": True,
        "requires_ocr_fallback": False,
    },
]

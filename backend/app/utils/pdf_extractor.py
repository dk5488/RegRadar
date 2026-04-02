"""
RegRadar — PDF Extraction Pipeline
Section 8: pdfplumber → pymupdf (fitz) → OCR (pytesseract) fallback.
"""

import io
from typing import Tuple
from app.core.logging import get_logger

logger = get_logger(__name__)

MIN_TEXT_THRESHOLD = 100  # characters — below this, try next method


async def extract_text_from_pdf(pdf_bytes: bytes) -> Tuple[str, str]:
    """
    Extract text from a PDF using a 3-step fallback pipeline.
    Returns: (extracted_text, method_used)
    """

    # Step 1: pdfplumber
    text = _try_pdfplumber(pdf_bytes)
    if text and len(text) >= MIN_TEXT_THRESHOLD:
        logger.info("PDF extracted via pdfplumber", chars=len(text))
        return text, "pdfplumber"

    # Step 2: pymupdf (fitz)
    text = _try_pymupdf(pdf_bytes)
    if text and len(text) >= MIN_TEXT_THRESHOLD:
        logger.info("PDF extracted via pymupdf", chars=len(text))
        return text, "pymupdf"

    # Step 3: OCR fallback
    text = _try_ocr(pdf_bytes)
    if text and len(text) >= MIN_TEXT_THRESHOLD:
        logger.info("PDF extracted via OCR", chars=len(text))
        return text, "ocr"

    logger.warning("PDF extraction failed — all methods returned insufficient text")
    return text or "", "failed"


def _try_pdfplumber(pdf_bytes: bytes) -> str:
    """Step 1: pdfplumber extraction."""
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n\n".join(text_parts)
    except Exception as e:
        logger.debug("pdfplumber failed", error=str(e))
        return ""


def _try_pymupdf(pdf_bytes: bytes) -> str:
    """Step 2: pymupdf (fitz) extraction."""
    try:
        import fitz  # pymupdf
        text_parts = []
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        return "\n\n".join(text_parts)
    except Exception as e:
        logger.debug("pymupdf failed", error=str(e))
        return ""


def _try_ocr(pdf_bytes: bytes) -> str:
    """Step 3: Render pages as images → pytesseract OCR."""
    try:
        from pdf2image import convert_from_bytes
        import pytesseract

        images = convert_from_bytes(pdf_bytes, dpi=300)
        text_parts = []
        for i, img in enumerate(images):
            page_text = pytesseract.image_to_string(img, lang="eng")
            if page_text.strip():
                text_parts.append(page_text)
        return "\n\n".join(text_parts)
    except Exception as e:
        logger.debug("OCR failed", error=str(e))
        return ""

"""
RegRadar — LLM Processing Service
Section 7: Structured extraction from regulatory documents using GPT-4o/Claude.
Implements the two prompt templates from the project context.
"""

import json
from typing import Optional
from app.core.config import get_settings
from app.core.logging import get_logger
from app.schemas.schemas import LLMExtractionResult

logger = get_logger(__name__)
settings = get_settings()

# ── Prompt Templates (Section 7) ─────────────────────────────────────

EXTRACTION_SYSTEM_PROMPT = (
    "You are a regulatory compliance expert specialising in Indian business law. "
    "You are given a raw text extract from an official Indian government notification, "
    "circular, or gazette entry. Your task is to extract structured information from "
    "this document. You must respond only with a valid JSON object — no preamble, "
    "no explanation, no markdown formatting. If you cannot determine a field with "
    "confidence, set its value to null and set confidence_score lower accordingly. "
    "Do not hallucinate or invent regulatory details. If the document does not "
    "contain enough information to complete a field, return null for that field."
)

EXTRACTION_USER_TEMPLATE = """Extract compliance information from the following regulatory document.

SOURCE: {source_name}
DOCUMENT DATE: {document_date}
RAW TEXT:
{raw_document_text}

Return a JSON object with exactly these fields:
{{
  "title": "short descriptive title of this regulatory change (max 10 words)",
  "summary_plain_english": "what changed, explained in plain language a non-lawyer MSME owner would understand (max 100 words)",
  "what_you_need_to_do": "specific action the business must take (max 60 words)",
  "affected_business_types": ["list of business types affected — use these categories only: All Businesses, GST Registered, Composition Scheme, Manufacturers, Exporters, Food Businesses, Businesses with 10+ Employees, Businesses with 20+ Employees, Private Limited Companies, LLPs, Sole Proprietors, NBFCs, Insurance Distributors, BIS Certified Manufacturers"],
  "effective_date": "YYYY-MM-DD or null",
  "compliance_deadline": "YYYY-MM-DD or null",
  "penalty_for_non_compliance": "penalty description in plain language or null",
  "regulatory_body": "name of the issuing government body",
  "notification_number": "official notification/circular number if present or null",
  "urgency_level": "one of: Critical, High, Medium, Low",
  "is_amendment_to_existing_rule": true or false,
  "confidence_score": a number between 0.0 and 1.0 representing your confidence in the extraction accuracy
}}"""

ALERT_SYSTEM_PROMPT = (
    "You are a compliance communication specialist. You write clear, friendly, "
    "actionable compliance alerts for small business owners in India who are not "
    "lawyers or accountants. Your writing must be simple (8th grade reading level), "
    "specific (tell them exactly what to do), and urgent without being alarming. "
    "Always end with a clear action item and deadline. Never use jargon. "
    "Respond only with the alert text — no preamble or explanation."
)

ALERT_USER_TEMPLATE = """Write a WhatsApp compliance alert for the following regulatory change.
The business receiving this alert is a {business_type} in the {industry_sector} sector with {employee_count_band} employees, GST status: {gst_status}.

REGULATORY CHANGE DETAILS:
Title: {title}
What changed: {summary_plain_english}
What they need to do: {what_you_need_to_do}
Deadline: {compliance_deadline}
Penalty if missed: {penalty_for_non_compliance}

Write the alert in {preferred_language}. Keep it under 300 words.
Format:
Line 1: Emoji + Alert title (e.g. '📋 GST Filing Rule Change')
Line 2: Blank
Line 3-5: What changed (2-3 sentences max)
Line 6: Blank
Line 7-8: What you need to do
Line 9: Blank
Line 10: Deadline: [date]
Line 11: Penalty if missed: [penalty]
Line 12: Blank
Line 13: 'Reply DONE when complete or HELP if you need assistance.'"""


# ── LLM Client Abstraction ───────────────────────────────────────────

async def _call_openai(system_prompt: str, user_prompt: str) -> str:
    """Call OpenAI GPT-4o for structured extraction."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    response = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,  # Low temperature for factual extraction
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content


async def _call_anthropic(system_prompt: str, user_prompt: str) -> str:
    """Call Anthropic Claude for structured extraction."""
    from anthropic import AsyncAnthropic

    client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )

    return response.content[0].text


async def _call_llm(system_prompt: str, user_prompt: str) -> str:
    """Route to the configured LLM provider."""
    if settings.LLM_PROVIDER == "anthropic":
        return await _call_anthropic(system_prompt, user_prompt)
    return await _call_openai(system_prompt, user_prompt)


# ── Public API ────────────────────────────────────────────────────────

async def extract_regulatory_content(
    raw_text: str,
    source_name: str,
    document_date: str,
) -> LLMExtractionResult:
    """
    Process a raw regulatory document through the LLM extraction pipeline.
    Section 7, Prompt Template 1.

    Args:
        raw_text: The extracted text from the regulatory document.
        source_name: Name of the data source (e.g. "CBIC / GST Council").
        document_date: The date of the document (YYYY-MM-DD).

    Returns:
        LLMExtractionResult with structured fields.
    """
    # Truncate very long documents to stay within token limits (~8000 words)
    max_chars = 32_000
    if len(raw_text) > max_chars:
        logger.warning(
            "Document truncated for LLM processing",
            original_length=len(raw_text),
            truncated_to=max_chars,
        )
        raw_text = raw_text[:max_chars]

    user_prompt = EXTRACTION_USER_TEMPLATE.format(
        source_name=source_name,
        document_date=document_date,
        raw_document_text=raw_text,
    )

    logger.info(
        "Sending document to LLM",
        source=source_name,
        provider=settings.LLM_PROVIDER,
        text_length=len(raw_text),
    )

    raw_response = await _call_llm(EXTRACTION_SYSTEM_PROMPT, user_prompt)

    try:
        parsed = json.loads(raw_response)
        result = LLMExtractionResult(**parsed)
        logger.info(
            "LLM extraction complete",
            title=result.title,
            confidence=result.confidence_score,
        )
        return result
    except (json.JSONDecodeError, Exception) as e:
        logger.error("Failed to parse LLM response", error=str(e), raw=raw_response[:500])
        # Return a low-confidence empty result so it goes to priority review
        return LLMExtractionResult(confidence_score=0.0)


async def generate_alert_text(
    title: str,
    summary_plain_english: str,
    what_you_need_to_do: str,
    compliance_deadline: Optional[str],
    penalty_for_non_compliance: Optional[str],
    business_type: str,
    industry_sector: str,
    employee_count_band: str,
    gst_status: str,
    preferred_language: str = "English",
) -> str:
    """
    Generate a personalised WhatsApp/email alert message.
    Section 7, Prompt Template 2.

    Returns:
        Plain-text alert message ready for delivery.
    """
    user_prompt = ALERT_USER_TEMPLATE.format(
        business_type=business_type,
        industry_sector=industry_sector,
        employee_count_band=employee_count_band,
        gst_status=gst_status,
        title=title,
        summary_plain_english=summary_plain_english,
        what_you_need_to_do=what_you_need_to_do,
        compliance_deadline=compliance_deadline or "No specific deadline",
        penalty_for_non_compliance=penalty_for_non_compliance or "Not specified",
        preferred_language=preferred_language,
    )

    return await _call_llm(ALERT_SYSTEM_PROMPT, user_prompt)

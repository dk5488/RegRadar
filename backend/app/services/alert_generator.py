"""
RegRadar — Alert Generation Service
Section 6, Component 7: Creates alerts for matching businesses and
enqueues them for multi-channel delivery.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.logging import get_logger
from app.models.models import (
    Alert, BusinessProfile, ComplianceItem, DeliveryLog,
)
from app.models.enums import AlertStatus, DeliveryChannel, PreferredLanguage
from app.services.applicability_engine import find_applicable_profiles
from app.services.llm_processor import generate_alert_text

logger = get_logger(__name__)


async def generate_alerts_for_compliance_item(
    compliance_item: ComplianceItem,
    db: AsyncSession,
) -> List[Alert]:
    """
    Generate personalised alerts for all applicable business profiles.

    Flow (Section 6, Stage 7):
      1. Run applicability engine to find matching profiles
      2. For each profile, generate personalised alert text via LLM
      3. Create Alert records (one per compliance item + profile pair)
      4. Return created alerts for delivery enqueuing

    The UniqueConstraint (compliance_item_id, business_profile_id)
    prevents duplicate alerts.
    """
    # Step 1: Find all matching profiles
    matched_profiles = await find_applicable_profiles(compliance_item, db)

    if not matched_profiles:
        logger.info(
            "No matching profiles for compliance item",
            compliance_id=compliance_item.compliance_id,
        )
        return []

    created_alerts = []

    for profile in matched_profiles:
        # Check if alert already exists for this pair
        existing = await db.execute(
            select(Alert).where(
                Alert.compliance_item_id == compliance_item.id,
                Alert.business_profile_id == profile.id,
            )
        )
        if existing.scalar_one_or_none():
            logger.debug(
                "Alert already exists, skipping",
                compliance_id=compliance_item.compliance_id,
                business=profile.business_name,
            )
            continue

        # Step 2: Generate personalised alert text
        try:
            alert_body = await generate_alert_text(
                title=compliance_item.title,
                summary_plain_english=compliance_item.summary_plain_english or compliance_item.description or "",
                what_you_need_to_do=compliance_item.what_you_need_to_do or "",
                compliance_deadline=(
                    compliance_item.compliance_deadline.strftime("%Y-%m-%d")
                    if compliance_item.compliance_deadline else None
                ),
                penalty_for_non_compliance=compliance_item.penalty_for_non_compliance,
                business_type=profile.business_type.value,
                industry_sector=profile.industry_sector.value,
                employee_count_band=profile.employee_count_band.value,
                gst_status=profile.gst_status.value,
                preferred_language=profile.preferred_language.value,
            )
        except Exception as e:
            logger.error(
                "Failed to generate alert text via LLM, using fallback",
                error=str(e),
                compliance_id=compliance_item.compliance_id,
                business=profile.business_name,
            )
            # Fallback to a structured but non-LLM alert
            alert_body = _build_fallback_alert(compliance_item)

        # Step 3: Create Alert record
        alert = Alert(
            compliance_item_id=compliance_item.id,
            business_profile_id=profile.id,
            alert_title=f"📋 {compliance_item.title}",
            alert_body=alert_body,
            language=profile.preferred_language,
            status=AlertStatus.PENDING,
        )
        db.add(alert)
        created_alerts.append(alert)

    if created_alerts:
        await db.flush()
        for alert in created_alerts:
            await db.refresh(alert)

    logger.info(
        "Alert generation complete",
        compliance_id=compliance_item.compliance_id,
        matched_profiles=len(matched_profiles),
        alerts_created=len(created_alerts),
    )

    return created_alerts


async def create_delivery_logs_for_alert(
    alert: Alert,
    profile: BusinessProfile,
    db: AsyncSession,
) -> List[DeliveryLog]:
    """
    Create DeliveryLog entries for each channel the user has opted into.

    Reads the profile's alert_channels and creates one DeliveryLog per channel.
    """
    logs = []
    channels = profile.alert_channels or ["Email"]

    for channel_str in channels:
        channel_str_lower = channel_str.lower()

        if channel_str_lower == "whatsapp" and profile.whatsapp_number:
            log = DeliveryLog(
                alert_id=alert.id,
                channel=DeliveryChannel.WHATSAPP,
                recipient=profile.whatsapp_number,
            )
        elif channel_str_lower == "email" and profile.email_address:
            log = DeliveryLog(
                alert_id=alert.id,
                channel=DeliveryChannel.EMAIL,
                recipient=profile.email_address,
            )
        elif channel_str_lower == "sms" and profile.whatsapp_number:
            log = DeliveryLog(
                alert_id=alert.id,
                channel=DeliveryChannel.SMS,
                recipient=profile.whatsapp_number,
            )
        else:
            continue

        db.add(log)
        logs.append(log)

    if logs:
        await db.flush()

    return logs


def _build_fallback_alert(item: ComplianceItem) -> str:
    """Build a structured alert without LLM when the LLM call fails."""
    deadline = (
        item.compliance_deadline.strftime("%d %B %Y")
        if item.compliance_deadline else "Not specified"
    )
    penalty = item.penalty_for_non_compliance or "Not specified"

    return (
        f"📋 {item.title}\n\n"
        f"{item.summary_plain_english or item.description or 'A new regulatory update has been published.'}\n\n"
        f"What you need to do: {item.what_you_need_to_do or 'Please review the notification.'}\n\n"
        f"Deadline: {deadline}\n"
        f"Penalty if missed: {penalty}\n\n"
        f"⚠️ This alert is for informational purposes only. "
        f"Please consult your CA or legal advisor before taking compliance action.\n\n"
        f"Reply DONE when complete or HELP if you need assistance."
    )

"""
RegRadar — Applicability Engine
Section 5 & 6 (Component 6): Matches compliance items against business profiles
using the JSONB applicability matrix.

The engine evaluates:
  1. `applicable_if` — positive-match rules (all conditions must be satisfied)
  2. `not_applicable_if` — exclusion rules (any match disqualifies)
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.logging import get_logger
from app.models.models import BusinessProfile, ComplianceItem

logger = get_logger(__name__)


def _profile_matches_rules(profile: BusinessProfile, rules: dict) -> bool:
    """
    Check if a business profile matches a set of applicability rules.

    Rules are a dict like:
      {"gst_status": ["Registered (Regular)"], "annual_turnover_band": ["₹5Cr–₹10Cr"]}

    A profile matches if ALL keys in the rules dict match at least one value.
    (AND logic across keys, OR logic within a key's value list)
    """
    if not rules:
        return True  # No rules = applies to everyone

    for field_name, allowed_values in rules.items():
        if not allowed_values:
            continue

        # "ALL" wildcard
        if "ALL" in allowed_values:
            continue

        profile_value = getattr(profile, field_name, None)

        if profile_value is None:
            return False

        # Handle JSONB array fields (operating_states, existing_licences)
        if isinstance(profile_value, list):
            # At least one value in the profile must be in allowed_values
            if not any(v in allowed_values for v in profile_value):
                return False
        else:
            # Enum fields — compare by .value if it's an enum
            actual_value = profile_value.value if hasattr(profile_value, "value") else str(profile_value)
            if actual_value not in allowed_values:
                return False

    return True


async def find_applicable_profiles(
    compliance_item: ComplianceItem,
    db: AsyncSession,
    ca_firm_id: Optional[UUID] = None,
) -> List[BusinessProfile]:
    """
    Given a compliance item, find all business profiles it applies to.

    Section 5 matching algorithm:
      1. For each BusinessProfile, check applicable_if rules
      2. If match, check not_applicable_if exclusions
      3. If still matched, include in results

    Args:
        compliance_item: The compliance item with applicable_if / not_applicable_if rules.
        db: Database session.
        ca_firm_id: Optional — limit matching to a specific CA firm's clients.

    Returns:
        List of matching BusinessProfile objects.
    """
    query = select(BusinessProfile).where(BusinessProfile.is_active == True)

    if ca_firm_id:
        query = query.where(BusinessProfile.ca_firm_id == ca_firm_id)

    result = await db.execute(query)
    all_profiles = result.scalars().all()

    applicable_if = compliance_item.applicable_if or {}
    not_applicable_if = compliance_item.not_applicable_if or {}

    matched_profiles = []

    for profile in all_profiles:
        # Step 1: Check positive match
        if not _profile_matches_rules(profile, applicable_if):
            continue

        # Step 2: Check exclusion rules
        if not_applicable_if and _profile_matches_rules(profile, not_applicable_if):
            continue

        matched_profiles.append(profile)

    logger.info(
        "Applicability matching complete",
        compliance_id=compliance_item.compliance_id,
        total_profiles=len(all_profiles),
        matched=len(matched_profiles),
    )

    return matched_profiles


async def check_profile_applicability(
    profile: BusinessProfile,
    db: AsyncSession,
) -> List[ComplianceItem]:
    """
    Reverse lookup: given a business profile, find all compliance items
    that apply to it. Useful for onboarding — immediately show a new
    business which rules they need to follow.

    Args:
        profile: The business profile to check.
        db: Database session.

    Returns:
        List of applicable ComplianceItem objects.
    """
    result = await db.execute(
        select(ComplianceItem).where(
            ComplianceItem.is_active == True,
            ComplianceItem.is_verified == True,
        )
    )
    all_items = result.scalars().all()

    applicable_items = []

    for item in all_items:
        applicable_if = item.applicable_if or {}
        not_applicable_if = item.not_applicable_if or {}

        if not _profile_matches_rules(profile, applicable_if):
            continue

        if not_applicable_if and _profile_matches_rules(profile, not_applicable_if):
            continue

        applicable_items.append(item)

    logger.info(
        "Profile applicability check complete",
        business=profile.business_name,
        total_items=len(all_items),
        applicable=len(applicable_items),
    )

    return applicable_items

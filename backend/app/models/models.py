"""
RegRadar — SQLAlchemy ORM Models
Complete database model layer matching the project context document.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float,
    DateTime, ForeignKey, Enum, Index, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import (
    BusinessType, IndustrySector, IndianState, UdyamCategory,
    EmployeeCountBand, TurnoverBand, GSTStatus, PreferredLanguage,
    AlertChannel, DocumentStatus, UrgencyLevel, AlertStatus,
    DeliveryChannel, UserRole, SubscriptionTier,
)


def utcnow():
    return datetime.now(timezone.utc)


# ═══════════════════════════════════════════════════════════════════════
#  USERS & AUTH
# ═══════════════════════════════════════════════════════════════════════

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.MSME_OWNER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Relationships
    ca_firm_id = Column(UUID(as_uuid=True), ForeignKey("ca_firms.id"), nullable=True)
    ca_firm = relationship("CAFirm", back_populates="users")

    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


# ═══════════════════════════════════════════════════════════════════════
#  CA FIRMS
# ═══════════════════════════════════════════════════════════════════════

class CAFirm(Base):
    __tablename__ = "ca_firms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firm_name = Column(String(255), nullable=False)
    registration_number = Column(String(50), nullable=True)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(Enum(IndianState), nullable=True)

    # Subscription
    subscription_tier = Column(
        Enum(SubscriptionTier), default=SubscriptionTier.CA_STARTER
    )
    max_client_profiles = Column(Integer, default=25)
    is_active = Column(Boolean, default=True)

    # White-label
    custom_brand_name = Column(String(255), nullable=True)
    custom_domain = Column(String(255), nullable=True)
    logo_url = Column(String(500), nullable=True)

    # Relationships
    users = relationship("User", back_populates="ca_firm")
    business_profiles = relationship("BusinessProfile", back_populates="ca_firm")

    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


# ═══════════════════════════════════════════════════════════════════════
#  BUSINESS PROFILES (Section 3 — all 19 fields)
# ═══════════════════════════════════════════════════════════════════════

class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Field 1 — business_name
    business_name = Column(String(255), nullable=False)

    # Field 2 — business_type
    business_type = Column(Enum(BusinessType), nullable=False)

    # Field 3 — industry_sector
    industry_sector = Column(Enum(IndustrySector), nullable=False)
    industry_sector_other = Column(String(255), nullable=True)  # free-text fallback

    # Field 4 — nic_code (optional)
    nic_code = Column(String(10), nullable=True)

    # Field 5 — registration_state
    registration_state = Column(Enum(IndianState), nullable=False)

    # Field 6 — operating_states (multi-select, stored as JSONB array)
    operating_states = Column(JSONB, nullable=False, default=list)

    # Field 7 — udyam_category
    udyam_category = Column(Enum(UdyamCategory), nullable=False)

    # Field 8 — employee_count_band
    employee_count_band = Column(Enum(EmployeeCountBand), nullable=False)

    # Field 9 — annual_turnover_band
    annual_turnover_band = Column(Enum(TurnoverBand), nullable=False)

    # Field 10 — gst_status
    gst_status = Column(Enum(GSTStatus), nullable=False)

    # Field 11 — has_export_activity
    has_export_activity = Column(Boolean, default=False)

    # Field 12 — has_manufacturing_unit
    has_manufacturing_unit = Column(Boolean, default=False)

    # Field 13 — handles_food_products
    handles_food_products = Column(Boolean, default=False)

    # Field 14 — existing_licences (multi-select, stored as JSONB array)
    existing_licences = Column(JSONB, nullable=False, default=list)

    # Field 15 — ca_firm_id (optional)
    ca_firm_id = Column(UUID(as_uuid=True), ForeignKey("ca_firms.id"), nullable=True)
    ca_firm = relationship("CAFirm", back_populates="business_profiles")

    # Field 16 — preferred_language
    preferred_language = Column(
        Enum(PreferredLanguage), default=PreferredLanguage.ENGLISH
    )

    # Field 17 — alert_channels (multi-select, JSONB array)
    alert_channels = Column(JSONB, nullable=False, default=["Email"])

    # Field 18 — whatsapp_number
    whatsapp_number = Column(String(20), nullable=True)

    # Field 19 — email_address
    email_address = Column(String(255), nullable=False)

    # Ownership
    owner_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    alerts = relationship("Alert", back_populates="business_profile")

    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_bp_registration_state", "registration_state"),
        Index("ix_bp_business_type", "business_type"),
        Index("ix_bp_gst_status", "gst_status"),
        Index("ix_bp_ca_firm", "ca_firm_id"),
    )


# ═══════════════════════════════════════════════════════════════════════
#  REGULATORY SOURCES (Section 4)
# ═══════════════════════════════════════════════════════════════════════

class Source(Base):
    __tablename__ = "sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    short_code = Column(String(20), nullable=False, unique=True)  # e.g. "MCA", "CBIC"
    base_url = Column(String(500), nullable=False)
    secondary_urls = Column(JSONB, nullable=True, default=list)  # additional URLs
    fetch_method = Column(String(50), nullable=False, default="http_scraper")  # http_scraper | rss | api
    fetch_frequency_hours = Column(Integer, nullable=False, default=24)
    scraper_module_name = Column(String(100), nullable=False)  # e.g. "mca_scraper"
    requires_pdf_extraction = Column(Boolean, default=True)
    requires_ocr_fallback = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Health
    last_fetched_at = Column(DateTime(timezone=True), nullable=True)
    last_successful_fetch_at = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(Text, nullable=True)
    consecutive_failures = Column(Integer, default=0)

    # Relationships
    documents = relationship("Document", back_populates="source")

    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


# ═══════════════════════════════════════════════════════════════════════
#  DOCUMENTS (fetched regulatory content)
# ═══════════════════════════════════════════════════════════════════════

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)
    source = relationship("Source", back_populates="documents")

    url = Column(String(1000), nullable=False)
    title = Column(String(500), nullable=True)

    # Content
    raw_text = Column(Text, nullable=True)
    content_hash = Column(String(64), nullable=True)  # SHA-256
    previous_hash = Column(String(64), nullable=True)
    raw_pdf_s3_key = Column(String(500), nullable=True)  # S3 key for raw PDF

    # Extraction metadata
    extraction_method = Column(String(50), nullable=True)  # pdfplumber | pymupdf | ocr | html
    page_count = Column(Integer, nullable=True)
    word_count = Column(Integer, nullable=True)

    # Processing state
    status = Column(Enum(DocumentStatus), default=DocumentStatus.FETCHED)
    processing_error = Column(Text, nullable=True)

    # LLM extraction output (stored as JSONB)
    llm_extraction = Column(JSONB, nullable=True)
    confidence_score = Column(Float, nullable=True)

    # CA review
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    review_notes = Column(Text, nullable=True)
    approved_extraction = Column(JSONB, nullable=True)  # final version after CA edit

    # Timing
    fetched_at = Column(DateTime(timezone=True), default=utcnow)
    first_seen_at = Column(DateTime(timezone=True), default=utcnow)
    last_changed_at = Column(DateTime(timezone=True), nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    compliance_item = relationship("ComplianceItem", back_populates="source_document", uselist=False)

    __table_args__ = (
        Index("ix_doc_source_url", "source_id", "url"),
        Index("ix_doc_status", "status"),
        Index("ix_doc_content_hash", "content_hash"),
    )


# ═══════════════════════════════════════════════════════════════════════
#  COMPLIANCE ITEMS — Applicability Matrix (Section 5)
# ═══════════════════════════════════════════════════════════════════════

class ComplianceItem(Base):
    __tablename__ = "compliance_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    compliance_id = Column(String(20), nullable=False, unique=True)  # e.g. "GST-001"

    # Content
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    summary_plain_english = Column(Text, nullable=True)
    what_you_need_to_do = Column(Text, nullable=True)

    # Regulatory reference
    regulatory_body = Column(String(100), nullable=False)
    regulation_reference = Column(String(300), nullable=True)
    notification_number = Column(String(100), nullable=True)

    # Applicability rules (JSONB — see Section 5 structure)
    applicable_if = Column(JSONB, nullable=False, default=dict)
    not_applicable_if = Column(JSONB, nullable=True, default=dict)

    # Scheduling
    frequency = Column(String(50), nullable=True)  # Monthly, Quarterly, Annual, One-time
    due_date_logic = Column(String(300), nullable=True)
    alert_trigger_days_before = Column(JSONB, nullable=True, default=[30, 7, 1])

    # Penalty
    penalty_for_non_compliance = Column(Text, nullable=True)

    # Urgency
    urgency_level = Column(Enum(UrgencyLevel), default=UrgencyLevel.MEDIUM)
    effective_date = Column(DateTime(timezone=True), nullable=True)
    compliance_deadline = Column(DateTime(timezone=True), nullable=True)

    # Source link
    source_document_id = Column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True
    )
    source_document = relationship("Document", back_populates="compliance_item")

    # Amendment tracking
    is_amendment = Column(Boolean, default=False)
    amends_compliance_id = Column(String(20), nullable=True)

    # Verification
    is_verified = Column(Boolean, default=False)
    verified_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)

    is_active = Column(Boolean, default=True)

    # Relationships
    alerts = relationship("Alert", back_populates="compliance_item")

    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_ci_regulatory_body", "regulatory_body"),
        Index("ix_ci_urgency", "urgency_level"),
        Index("ix_ci_deadline", "compliance_deadline"),
    )


# ═══════════════════════════════════════════════════════════════════════
#  ALERTS — Personalised delivery to businesses
# ═══════════════════════════════════════════════════════════════════════

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Links
    compliance_item_id = Column(
        UUID(as_uuid=True), ForeignKey("compliance_items.id"), nullable=False
    )
    compliance_item = relationship("ComplianceItem", back_populates="alerts")

    business_profile_id = Column(
        UUID(as_uuid=True), ForeignKey("business_profiles.id"), nullable=False
    )
    business_profile = relationship("BusinessProfile", back_populates="alerts")

    # Content (generated per-profile, may be in user's preferred language)
    alert_title = Column(String(300), nullable=False)
    alert_body = Column(Text, nullable=False)
    language = Column(Enum(PreferredLanguage), default=PreferredLanguage.ENGLISH)

    # Status
    status = Column(Enum(AlertStatus), default=AlertStatus.PENDING)
    acknowledgement_note = Column(Text, nullable=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    # Relationships
    delivery_logs = relationship("DeliveryLog", back_populates="alert")

    __table_args__ = (
        Index("ix_alert_business", "business_profile_id"),
        Index("ix_alert_status", "status"),
        Index("ix_alert_compliance", "compliance_item_id"),
        UniqueConstraint(
            "compliance_item_id", "business_profile_id",
            name="uq_alert_compliance_business"
        ),
    )


# ═══════════════════════════════════════════════════════════════════════
#  DELIVERY LOGS — Track WhatsApp / Email / SMS delivery
# ═══════════════════════════════════════════════════════════════════════

class DeliveryLog(Base):
    __tablename__ = "delivery_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    alert_id = Column(UUID(as_uuid=True), ForeignKey("alerts.id"), nullable=False)
    alert = relationship("Alert", back_populates="delivery_logs")

    channel = Column(Enum(DeliveryChannel), nullable=False)
    recipient = Column(String(255), nullable=False)  # phone or email

    # Status tracking
    sent_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    failed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)

    # External IDs (from BSP / SendGrid)
    external_message_id = Column(String(255), nullable=True)
    retry_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=utcnow)

    __table_args__ = (
        Index("ix_dl_alert", "alert_id"),
        Index("ix_dl_channel", "channel"),
    )


# ═══════════════════════════════════════════════════════════════════════
#  SCRAPER HEALTH — Monitoring (Section 9 of context)
# ═══════════════════════════════════════════════════════════════════════

class ScraperRun(Base):
    __tablename__ = "scraper_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)

    started_at = Column(DateTime(timezone=True), default=utcnow)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    success = Column(Boolean, nullable=True)
    documents_found = Column(Integer, default=0)
    new_documents = Column(Integer, default=0)
    changed_documents = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    duration_seconds = Column(Float, nullable=True)

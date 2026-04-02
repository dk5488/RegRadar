"""
RegRadar — Pydantic Schemas
Request/response validation schemas for the API layer.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.models.enums import (
    BusinessType, IndustrySector, IndianState, UdyamCategory,
    EmployeeCountBand, TurnoverBand, GSTStatus, PreferredLanguage,
    AlertChannel, LicenceType, UrgencyLevel, AlertStatus, UserRole,
    SubscriptionTier, DocumentStatus,
)


# ═══════════════════════════════════════════════════════════════════════
#  AUTH
# ═══════════════════════════════════════════════════════════════════════

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=255)
    phone: Optional[str] = None
    role: UserRole = UserRole.MSME_OWNER


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    phone: Optional[str]
    role: UserRole
    is_active: bool
    is_verified: bool
    ca_firm_id: Optional[UUID]
    created_at: datetime

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════════════════
#  CA FIRM
# ═══════════════════════════════════════════════════════════════════════

class CAFirmCreate(BaseModel):
    firm_name: str = Field(min_length=1, max_length=255)
    registration_number: Optional[str] = None
    contact_email: EmailStr
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[IndianState] = None
    subscription_tier: SubscriptionTier = SubscriptionTier.CA_STARTER


class CAFirmResponse(BaseModel):
    id: UUID
    firm_name: str
    registration_number: Optional[str]
    contact_email: str
    contact_phone: Optional[str]
    state: Optional[IndianState]
    subscription_tier: SubscriptionTier
    max_client_profiles: int
    is_active: bool
    custom_brand_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════════════════
#  BUSINESS PROFILE (Section 3 — all fields)
# ═══════════════════════════════════════════════════════════════════════

class BusinessProfileCreate(BaseModel):
    """Onboarding form — all 19 fields from Section 3."""
    business_name: str = Field(min_length=1, max_length=255)
    business_type: BusinessType
    industry_sector: IndustrySector
    industry_sector_other: Optional[str] = None
    nic_code: Optional[str] = None
    registration_state: IndianState
    operating_states: List[IndianState] = []
    udyam_category: UdyamCategory
    employee_count_band: EmployeeCountBand
    annual_turnover_band: TurnoverBand
    gst_status: GSTStatus
    has_export_activity: bool = False
    has_manufacturing_unit: bool = False
    handles_food_products: bool = False
    existing_licences: List[LicenceType] = []
    preferred_language: PreferredLanguage = PreferredLanguage.ENGLISH
    alert_channels: List[AlertChannel] = [AlertChannel.EMAIL]
    whatsapp_number: Optional[str] = None
    email_address: EmailStr

    @field_validator("operating_states", mode="before")
    @classmethod
    def ensure_registration_state_in_operating(cls, v, info):
        """Registration state should always be in operating states."""
        reg_state = info.data.get("registration_state")
        if reg_state and reg_state not in v:
            v = [reg_state] + list(v)
        return v


class BusinessProfileUpdate(BaseModel):
    """Partial update — all fields optional."""
    business_name: Optional[str] = None
    business_type: Optional[BusinessType] = None
    industry_sector: Optional[IndustrySector] = None
    industry_sector_other: Optional[str] = None
    nic_code: Optional[str] = None
    registration_state: Optional[IndianState] = None
    operating_states: Optional[List[IndianState]] = None
    udyam_category: Optional[UdyamCategory] = None
    employee_count_band: Optional[EmployeeCountBand] = None
    annual_turnover_band: Optional[TurnoverBand] = None
    gst_status: Optional[GSTStatus] = None
    has_export_activity: Optional[bool] = None
    has_manufacturing_unit: Optional[bool] = None
    handles_food_products: Optional[bool] = None
    existing_licences: Optional[List[LicenceType]] = None
    preferred_language: Optional[PreferredLanguage] = None
    alert_channels: Optional[List[AlertChannel]] = None
    whatsapp_number: Optional[str] = None
    email_address: Optional[EmailStr] = None


class BusinessProfileResponse(BaseModel):
    id: UUID
    business_name: str
    business_type: BusinessType
    industry_sector: IndustrySector
    industry_sector_other: Optional[str]
    nic_code: Optional[str]
    registration_state: IndianState
    operating_states: list
    udyam_category: UdyamCategory
    employee_count_band: EmployeeCountBand
    annual_turnover_band: TurnoverBand
    gst_status: GSTStatus
    has_export_activity: bool
    has_manufacturing_unit: bool
    handles_food_products: bool
    existing_licences: list
    preferred_language: PreferredLanguage
    alert_channels: list
    whatsapp_number: Optional[str]
    email_address: str
    ca_firm_id: Optional[UUID]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════════════════
#  COMPLIANCE ITEMS
# ═══════════════════════════════════════════════════════════════════════

class ComplianceItemCreate(BaseModel):
    compliance_id: str = Field(max_length=20)
    title: str = Field(max_length=300)
    description: Optional[str] = None
    summary_plain_english: Optional[str] = None
    what_you_need_to_do: Optional[str] = None
    regulatory_body: str = Field(max_length=100)
    regulation_reference: Optional[str] = None
    notification_number: Optional[str] = None
    applicable_if: dict = {}
    not_applicable_if: Optional[dict] = {}
    frequency: Optional[str] = None
    due_date_logic: Optional[str] = None
    alert_trigger_days_before: List[int] = [30, 7, 1]
    penalty_for_non_compliance: Optional[str] = None
    urgency_level: UrgencyLevel = UrgencyLevel.MEDIUM
    effective_date: Optional[datetime] = None
    compliance_deadline: Optional[datetime] = None
    is_amendment: bool = False
    amends_compliance_id: Optional[str] = None


class ComplianceItemResponse(BaseModel):
    id: UUID
    compliance_id: str
    title: str
    description: Optional[str]
    summary_plain_english: Optional[str]
    what_you_need_to_do: Optional[str]
    regulatory_body: str
    regulation_reference: Optional[str]
    applicable_if: dict
    not_applicable_if: Optional[dict]
    frequency: Optional[str]
    due_date_logic: Optional[str]
    penalty_for_non_compliance: Optional[str]
    urgency_level: UrgencyLevel
    effective_date: Optional[datetime]
    compliance_deadline: Optional[datetime]
    is_amendment: bool
    is_verified: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════════════════
#  LLM EXTRACTION (from processed document)
# ═══════════════════════════════════════════════════════════════════════

class LLMExtractionResult(BaseModel):
    """JSON output from the LLM regulatory document extraction prompt."""
    title: Optional[str] = None
    summary_plain_english: Optional[str] = None
    what_you_need_to_do: Optional[str] = None
    affected_business_types: Optional[List[str]] = None
    effective_date: Optional[str] = None
    compliance_deadline: Optional[str] = None
    penalty_for_non_compliance: Optional[str] = None
    regulatory_body: Optional[str] = None
    notification_number: Optional[str] = None
    urgency_level: Optional[str] = None
    is_amendment_to_existing_rule: Optional[bool] = None
    confidence_score: Optional[float] = None


# ═══════════════════════════════════════════════════════════════════════
#  ALERTS
# ═══════════════════════════════════════════════════════════════════════

class AlertResponse(BaseModel):
    id: UUID
    compliance_item_id: UUID
    business_profile_id: UUID
    alert_title: str
    alert_body: str
    language: PreferredLanguage
    status: AlertStatus
    acknowledgement_note: Optional[str]
    acknowledged_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class AlertAcknowledge(BaseModel):
    status: AlertStatus  # noted, done, not_applicable
    note: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════
#  DOCUMENTS
# ═══════════════════════════════════════════════════════════════════════

class DocumentResponse(BaseModel):
    id: UUID
    source_id: UUID
    url: str
    title: Optional[str]
    status: DocumentStatus
    confidence_score: Optional[float]
    llm_extraction: Optional[dict]
    fetched_at: datetime
    processed_at: Optional[datetime]
    reviewed_at: Optional[datetime]

    class Config:
        from_attributes = True


class DocumentReview(BaseModel):
    """CA reviewer action on a processed document."""
    action: str  # "approve", "edit", "reject"
    edited_extraction: Optional[dict] = None
    review_notes: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════
#  GENERIC
# ═══════════════════════════════════════════════════════════════════════

class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
    pages: int

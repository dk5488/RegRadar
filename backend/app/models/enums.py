"""
RegRadar — Enums
Shared enum types used across models, schemas, and business logic.
All enums match the project context document (Section 3 & 5).
"""

import enum


# ── Business Profile Enums ───────────────────────────────────────────

class BusinessType(str, enum.Enum):
    SOLE_PROPRIETORSHIP = "Sole Proprietorship"
    PARTNERSHIP_FIRM = "Partnership Firm"
    LLP = "LLP"
    PRIVATE_LIMITED = "Private Limited Company"
    PUBLIC_LIMITED = "Public Limited Company"
    HUF = "HUF"
    TRUST_SOCIETY = "Trust/Society"
    OPC = "One Person Company (OPC)"


class IndustrySector(str, enum.Enum):
    MANUFACTURING = "Manufacturing"
    TRADING_RETAIL = "Trading/Retail"
    FOOD_BEVERAGE = "Food & Beverage"
    IT_SOFTWARE = "IT/Software Services"
    PROFESSIONAL_SERVICES = "Professional Services"
    HEALTHCARE_PHARMA = "Healthcare/Pharma"
    CONSTRUCTION_REALESTATE = "Construction/Real Estate"
    LOGISTICS_TRANSPORT = "Logistics/Transport"
    FINANCIAL_SERVICES = "Financial Services"
    EDUCATION = "Education"
    AGRICULTURE = "Agriculture/Agro-processing"
    TEXTILE = "Textile"
    OTHER = "Other"


class IndianState(str, enum.Enum):
    ANDHRA_PRADESH = "Andhra Pradesh"
    ARUNACHAL_PRADESH = "Arunachal Pradesh"
    ASSAM = "Assam"
    BIHAR = "Bihar"
    CHHATTISGARH = "Chhattisgarh"
    GOA = "Goa"
    GUJARAT = "Gujarat"
    HARYANA = "Haryana"
    HIMACHAL_PRADESH = "Himachal Pradesh"
    JHARKHAND = "Jharkhand"
    KARNATAKA = "Karnataka"
    KERALA = "Kerala"
    MADHYA_PRADESH = "Madhya Pradesh"
    MAHARASHTRA = "Maharashtra"
    MANIPUR = "Manipur"
    MEGHALAYA = "Meghalaya"
    MIZORAM = "Mizoram"
    NAGALAND = "Nagaland"
    ODISHA = "Odisha"
    PUNJAB = "Punjab"
    RAJASTHAN = "Rajasthan"
    SIKKIM = "Sikkim"
    TAMIL_NADU = "Tamil Nadu"
    TELANGANA = "Telangana"
    TRIPURA = "Tripura"
    UTTAR_PRADESH = "Uttar Pradesh"
    UTTARAKHAND = "Uttarakhand"
    WEST_BENGAL = "West Bengal"
    # Union Territories
    ANDAMAN_NICOBAR = "Andaman and Nicobar Islands"
    CHANDIGARH = "Chandigarh"
    DADRA_NAGAR_HAVELI = "Dadra and Nagar Haveli and Daman and Diu"
    DELHI = "Delhi"
    JAMMU_KASHMIR = "Jammu and Kashmir"
    LADAKH = "Ladakh"
    LAKSHADWEEP = "Lakshadweep"
    PUDUCHERRY = "Puducherry"


class UdyamCategory(str, enum.Enum):
    MICRO = "Micro"
    SMALL = "Small"
    MEDIUM = "Medium"
    NOT_REGISTERED = "Not Registered"


class EmployeeCountBand(str, enum.Enum):
    BAND_0_5 = "0-5"
    BAND_6_10 = "6-10"
    BAND_11_20 = "11-20"
    BAND_21_50 = "21-50"
    BAND_51_100 = "51-100"
    BAND_101_200 = "101-200"
    BAND_200_PLUS = "200+"


class TurnoverBand(str, enum.Enum):
    BELOW_20L = "Below ₹20 lakh"
    L20_TO_L40 = "₹20L–₹40L"
    L40_TO_1_5CR = "₹40L–₹1.5Cr"
    CR1_5_TO_5CR = "₹1.5Cr–₹5Cr"
    CR5_TO_10CR = "₹5Cr–₹10Cr"
    CR10_TO_50CR = "₹10Cr–₹50Cr"
    ABOVE_50CR = "Above ₹50Cr"


class GSTStatus(str, enum.Enum):
    REGULAR = "Registered (Regular)"
    COMPOSITION = "Registered (Composition Scheme)"
    UNREGISTERED = "Unregistered"
    EXPORT_LUT = "Export-oriented (LUT holder)"
    SEZ = "SEZ unit"


class LicenceType(str, enum.Enum):
    FSSAI = "FSSAI"
    BIS = "BIS"
    IEC = "IEC"
    IRDAI = "IRDAI"
    DRUG_LICENCE = "Drug Licence"
    FACTORY_LICENCE = "Factory Licence"
    PESO = "PESO"
    MSME_UDYAM = "MSME Udyam"
    SHOPS_ESTABLISHMENTS = "Shops & Establishments"
    PROFESSIONAL_TAX = "Professional Tax Registration"
    OTHER = "Other"


class PreferredLanguage(str, enum.Enum):
    ENGLISH = "English"
    HINDI = "Hindi"
    KANNADA = "Kannada"
    TAMIL = "Tamil"
    TELUGU = "Telugu"
    MARATHI = "Marathi"
    GUJARATI = "Gujarati"


class AlertChannel(str, enum.Enum):
    WHATSAPP = "WhatsApp"
    EMAIL = "Email"
    SMS = "SMS"


# ── Document / Processing Enums ──────────────────────────────────────

class DocumentStatus(str, enum.Enum):
    FETCHED = "fetched"
    EXTRACTING = "extracting"
    EXTRACTED = "extracted"
    PROCESSING = "processing"
    PROCESSED = "processed"
    REVIEW_PENDING = "review_pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FAILED = "failed"


class UrgencyLevel(str, enum.Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class AlertStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    ACKNOWLEDGED_NOTED = "noted"
    ACKNOWLEDGED_DONE = "done"
    ACKNOWLEDGED_NOT_APPLICABLE = "not_applicable"
    FAILED = "failed"


class DeliveryChannel(str, enum.Enum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    SMS = "sms"


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CA_REVIEWER = "ca_reviewer"
    CA_FIRM_ADMIN = "ca_firm_admin"
    MSME_OWNER = "msme_owner"


class SubscriptionTier(str, enum.Enum):
    CA_STARTER = "ca_starter"
    CA_PROFESSIONAL = "ca_professional"
    CA_ENTERPRISE = "ca_enterprise"
    MSME_DIRECT = "msme_direct"

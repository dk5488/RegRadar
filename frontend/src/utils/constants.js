/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Constants
   Mirror of backend enums and app-wide configuration values.
   Keep in sync with backend/app/models/enums.py
   ═══════════════════════════════════════════════════════════════════════ */

// ── User Roles ──────────────────────────────────────────────────────────
export const USER_ROLES = {
  ADMIN: 'admin',
  CA_REVIEWER: 'ca_reviewer',
  CA_FIRM_ADMIN: 'ca_firm_admin',
  MSME_OWNER: 'msme_owner',
};

export const ROLE_LABELS = {
  [USER_ROLES.ADMIN]: 'Admin',
  [USER_ROLES.CA_REVIEWER]: 'CA Reviewer',
  [USER_ROLES.CA_FIRM_ADMIN]: 'CA Firm Admin',
  [USER_ROLES.MSME_OWNER]: 'MSME Owner',
};

// ── Business Types ──────────────────────────────────────────────────────
export const BUSINESS_TYPES = [
  'Sole Proprietorship',
  'Partnership Firm',
  'LLP',
  'Private Limited Company',
  'Public Limited Company',
  'HUF',
  'Trust/Society',
  'One Person Company (OPC)',
];

// ── Industry Sectors ────────────────────────────────────────────────────
export const INDUSTRY_SECTORS = [
  'Manufacturing',
  'Trading/Retail',
  'Food & Beverage',
  'IT/Software Services',
  'Professional Services',
  'Healthcare/Pharma',
  'Construction/Real Estate',
  'Logistics/Transport',
  'Financial Services',
  'Education',
  'Agriculture/Agro-processing',
  'Textile',
  'Other',
];

// ── Indian States & UTs ─────────────────────────────────────────────────
export const INDIAN_STATES = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
  'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
  'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
  'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
  'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
  'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
  'Andaman and Nicobar Islands', 'Chandigarh',
  'Dadra and Nagar Haveli and Daman and Diu', 'Delhi',
  'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry',
];

// ── Udyam Categories ────────────────────────────────────────────────────
export const UDYAM_CATEGORIES = ['Micro', 'Small', 'Medium', 'Not Registered'];

// ── Employee Count Bands ────────────────────────────────────────────────
export const EMPLOYEE_BANDS = ['0-5', '6-10', '11-20', '21-50', '51-100', '101-200', '200+'];

// ── Turnover Bands ──────────────────────────────────────────────────────
export const TURNOVER_BANDS = [
  'Below ₹20 lakh',
  '₹20L–₹40L',
  '₹40L–₹1.5Cr',
  '₹1.5Cr–₹5Cr',
  '₹5Cr–₹10Cr',
  '₹10Cr–₹50Cr',
  'Above ₹50Cr',
];

// ── GST Status ──────────────────────────────────────────────────────────
export const GST_STATUSES = [
  'Registered (Regular)',
  'Registered (Composition Scheme)',
  'Unregistered',
  'Export-oriented (LUT holder)',
  'SEZ unit',
];

// ── Licence Types ───────────────────────────────────────────────────────
export const LICENCE_TYPES = [
  'FSSAI', 'BIS', 'IEC', 'IRDAI', 'Drug Licence', 'Factory Licence',
  'PESO', 'MSME Udyam', 'Shops & Establishments',
  'Professional Tax Registration', 'Other',
];

// ── Languages ───────────────────────────────────────────────────────────
export const LANGUAGES = [
  'English', 'Hindi', 'Kannada', 'Tamil', 'Telugu', 'Marathi', 'Gujarati',
];

// ── Alert Channels ──────────────────────────────────────────────────────
export const ALERT_CHANNELS = ['WhatsApp', 'Email', 'SMS'];

// ── Alert Statuses ──────────────────────────────────────────────────────
export const ALERT_STATUSES = {
  PENDING: 'pending',
  SENT: 'sent',
  DELIVERED: 'delivered',
  READ: 'read',
  NOTED: 'noted',
  DONE: 'done',
  NOT_APPLICABLE: 'not_applicable',
  FAILED: 'failed',
};

export const ALERT_STATUS_LABELS = {
  pending: 'Pending',
  sent: 'Sent',
  delivered: 'Delivered',
  read: 'Read',
  noted: 'Noted',
  done: 'Done',
  not_applicable: 'N/A',
  failed: 'Failed',
};

// ── Urgency Levels ──────────────────────────────────────────────────────
export const URGENCY_LEVELS = {
  CRITICAL: 'Critical',
  HIGH: 'High',
  MEDIUM: 'Medium',
  LOW: 'Low',
};

// ── Document Statuses ───────────────────────────────────────────────────
export const DOCUMENT_STATUSES = {
  FETCHED: 'fetched',
  EXTRACTING: 'extracting',
  EXTRACTED: 'extracted',
  PROCESSING: 'processing',
  PROCESSED: 'processed',
  REVIEW_PENDING: 'review_pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  FAILED: 'failed',
};

// ── Subscription Tiers ──────────────────────────────────────────────────
export const SUBSCRIPTION_TIERS = {
  CA_STARTER: 'ca_starter',
  CA_PROFESSIONAL: 'ca_professional',
  CA_ENTERPRISE: 'ca_enterprise',
  MSME_DIRECT: 'msme_direct',
};

export const TIER_LABELS = {
  ca_starter: 'Starter',
  ca_professional: 'Professional',
  ca_enterprise: 'Enterprise',
  msme_direct: 'MSME Direct',
};

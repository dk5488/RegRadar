# RegRadar — Frontend Implementation Plan

> **Tech Stack**: Vite + React 18 · React Router v6 · Vanilla CSS (design tokens) · Axios · Recharts  
> **Branch Convention**: `F-<number>` starting from **F-28**  
> **Rule**: Pull latest `main` before creating each branch. One module = one branch = one PR.

---

## Phase 1 — Foundation & Design System

The scaffolding layer. Everything built here is consumed by every subsequent module.

| # | Module | Branch | Description |
|---|--------|--------|-------------|
| 1 | **Project Scaffold** | `F-28` | Init Vite + React app, folder structure (`/components`, `/pages`, `/hooks`, `/services`, `/context`, `/assets`, `/styles`), ESLint config, `.env` for API base URL, install dependencies (react-router-dom, axios, react-icons, recharts) |
| 2 | **Design System & Global CSS** | `F-29` | CSS custom properties (color palette, typography scale, spacing, shadows, border-radius, transitions), CSS reset, dark/light mode tokens, global utility classes, Google Fonts (Inter/Outfit) |
| 3 | **Shared Layout Shell** | `F-30` | `<AppLayout>` with collapsible sidebar, top navbar (user avatar, role badge, logout), `<Outlet>` for page routing, role-based nav items (MSME vs CA vs Admin), mobile hamburger menu, glassmorphism sidebar |
| 4 | **API Client & Auth Context** | `F-31` | Axios instance with interceptors (JWT attach, 401 redirect, refresh logic), `AuthContext` + `AuthProvider` (login, register, logout, me), `ProtectedRoute` component, role guard HOC, token persistence in localStorage |

---

## Phase 2 — Authentication & Onboarding

First user-facing flows. A user can register, log in, and complete the MSME business profile form.

| # | Module | Branch | Description |
|---|--------|--------|-------------|
| 5 | **Login & Register Pages** | `F-32` | Animated login/register forms with email + password, role selector (MSME Owner / CA Firm Admin), form validation, error toasts, redirect to dashboard on success, "forgot password" placeholder, premium glassmorphism card design |
| 6 | **Business Profile Onboarding Wizard** | `F-33` | Multi-step form (4 steps): **Step 1** — Business Identity (name, type, sector, NIC code); **Step 2** — Location & Size (registration state, operating states, udyam, employees, turnover); **Step 3** — Regulatory Flags (GST status, export, manufacturing, food, existing licences); **Step 4** — Preferences (language, alert channels, WhatsApp number, email). Progress stepper, validation per step, animated transitions, summary review before submit |

---

## Phase 3 — MSME Owner Dashboard

The core experience for an MSME user — alerts, compliance tracking, and profile management.

| # | Module | Branch | Description |
|---|--------|--------|-------------|
| 7 | **Alert Inbox** | `F-34` | Paginated alert list with urgency badges (Critical=red, High=orange, Medium=blue, Low=gray), status pills (pending, sent, delivered, noted, done), filter by status, search by title, sort by date/urgency, empty state illustration |
| 8 | **Alert Detail & Acknowledgement** | `F-35` | Full alert view: title, body (markdown rendered), compliance deadline countdown, penalty info, regulatory body badge. Action buttons: "Mark as Noted", "Mark as Done", "Not Applicable" with optional note textarea. Confirmation modal |
| 9 | **Compliance Calendar** | `F-36` | Monthly calendar grid showing upcoming compliance deadlines. Color-coded by urgency. Click a date to see alerts due. Mini sidebar showing "Next 7 days" upcoming items. Toggle between calendar and list view |
| 10 | **Business Profile Settings** | `F-37` | View and edit the user's business profile(s). Pre-filled form matching the onboarding fields. Inline validation. "Save Changes" with optimistic UI feedback. Danger zone for profile deactivation |

---

## Phase 4 — CA Firm Dashboard

Role-gated views for CA Firm Admins and CA Reviewers.

| # | Module | Branch | Description |
|---|--------|--------|-------------|
| 11 | **CA Dashboard Overview** | `F-38` | Summary cards: Active Clients count, Pending Alerts, Docs Awaiting Review, Acknowledged Alerts. Mini charts (alerts by urgency pie, alerts trend line). Quick actions: "Add Client", "Review Documents". Pulls from `/api/v1/ca/firms/{id}/dashboard` |
| 12 | **Client Portfolio Management** | `F-39` | Searchable, sortable table of all business profiles under the CA firm. Columns: name, business type, state, employee band, pending alerts count. Click row → view profile detail + their alerts. Bulk actions placeholder. "Add New Client" button → onboarding wizard pre-linked to CA firm |
| 13 | **Document Review Queue** | `F-40` | List of documents with status `review_pending`. Each card shows: source name, title, fetched date, confidence score badge (green >0.8, yellow 0.5–0.8, red <0.5). Click → review detail with LLM extraction JSON rendered as readable fields. Three action buttons: Approve, Edit & Approve (opens inline editor for extraction fields), Reject (with reason). Pulls from `/api/v1/documents?status_filter=review_pending` |

---

## Phase 5 — Admin Panel

Admin-only pages for system monitoring and management.

| # | Module | Branch | Description |
|---|--------|--------|-------------|
| 14 | **Scraper Health Monitor** | `F-41` | Grid of source cards showing: name, short code, last fetched time (with "X minutes ago" relative time), consecutive failures (red badge if >0), active/inactive toggle. Health indicator: green dot (healthy), yellow (stale), red (failing). Pulls from `/api/v1/health/sources` |
| 15 | **Scraper Run History** | `F-42` | Paginated table of scraper runs: source name, started time, duration, success/fail badge, docs found/new/changed counts, error message expandable. Filter by source. Pulls from `/api/v1/health/runs` |
| 16 | **User Management** | `F-43` | List all users (admin only), role badges, active/inactive status, CA firm association. Actions: activate/deactivate, change role (future API). Search by email/name |

---

## Phase 6 — Polish & Production Readiness

UX refinements, responsiveness, and production hardening.

| # | Module | Branch | Description |
|---|--------|--------|-------------|
| 17 | **Toast Notification System** | `F-44` | Global toast/notification component (success, error, warning, info). Auto-dismiss with progress bar. Stack up to 3 toasts. `useToast()` hook for triggering from anywhere. Replace all existing `alert()` calls |
| 18 | **Responsive & Mobile Optimization** | `F-45` | Media queries for all pages (breakpoints: 480px, 768px, 1024px, 1440px). Sidebar collapses to bottom nav on mobile. Tables become card lists on small screens. Touch-friendly tap targets (min 44px). Test all flows on mobile viewport |
| 19 | **Dark Mode Toggle** | `F-46` | Persistent dark/light mode toggle in navbar. CSS custom properties swap via `[data-theme="dark"]` on `<html>`. Store preference in localStorage. Smooth transition animation. Respect system preference on first visit (`prefers-color-scheme`) |
| 20 | **Loading States & Skeletons** | `F-47` | Skeleton loaders for all list/card views (pulsing placeholder blocks). Full-page loading spinner for route transitions. Inline button loading states (spinner replacing text). Error boundary component with retry button |
| 21 | **SEO & Meta Tags** | `F-48` | React Helmet for per-page title/description. Open Graph tags. Proper heading hierarchy on all pages. Semantic HTML audit. Favicon and manifest.json |
| 22 | **Production Build & Deployment Prep** | `F-49` | Environment-based API URL config, production build optimization, asset hashing, gzip compression check, Dockerfile for frontend container, CORS verification against backend |

---

## Folder Structure (Target)

```
frontend/
├── public/
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── assets/            # Static images, icons, illustrations
│   ├── components/        # Reusable UI components
│   │   ├── common/        # Button, Input, Modal, Toast, Card, Badge, Skeleton
│   │   ├── layout/        # AppLayout, Sidebar, Navbar, MobileNav
│   │   └── charts/        # Chart wrappers (Recharts)
│   ├── context/           # AuthContext, ThemeContext, ToastContext
│   ├── hooks/             # useAuth, useApi, useToast, useDebounce
│   ├── pages/             # Route-level page components
│   │   ├── auth/          # LoginPage, RegisterPage
│   │   ├── onboarding/    # OnboardingWizard
│   │   ├── msme/          # AlertInbox, AlertDetail, Calendar, ProfileSettings
│   │   ├── ca/            # CADashboard, ClientPortfolio, DocumentReview
│   │   └── admin/         # ScraperHealth, ScraperRuns, UserManagement
│   ├── services/          # API service modules (auth.js, profiles.js, alerts.js, etc.)
│   ├── styles/            # Global CSS, design tokens, component styles
│   │   ├── tokens.css     # CSS custom properties
│   │   ├── reset.css      # CSS reset/normalize
│   │   ├── global.css     # Global styles
│   │   └── components/    # Per-component CSS modules
│   ├── utils/             # Formatters, validators, constants
│   ├── App.jsx            # Router setup
│   └── main.jsx           # Entry point
├── .env
├── .env.example
├── index.html
├── package.json
└── vite.config.js
```

---

## Backend API Surface (Reference)

| Prefix | Endpoints | Used In |
|--------|-----------|---------|
| `/api/v1/auth` | `POST /register`, `POST /login`, `GET /me` | Phase 2 |
| `/api/v1/profiles` | `POST /`, `GET /`, `GET /{id}`, `PATCH /{id}`, `DELETE /{id}` | Phase 2, 3, 4 |
| `/api/v1/alerts` | `GET /`, `GET /{id}`, `POST /{id}/acknowledge` | Phase 3 |
| `/api/v1/compliance` | `POST /`, `GET /`, `GET /{id}` | Phase 3, 4 |
| `/api/v1/documents` | `GET /`, `GET /{id}`, `POST /{id}/review` | Phase 4 |
| `/api/v1/ca` | `POST /firms`, `GET /firms/{id}`, `GET /firms/{id}/dashboard` | Phase 4 |
| `/api/v1/health` | `GET /sources`, `GET /runs` | Phase 5 |

---

## Design Principles

1. **Premium Dark-First**: Deep slate backgrounds (#0f172a), vibrant accent gradients (indigo → cyan), glassmorphism cards with backdrop-blur
2. **Micro-Animations**: Hover lifts on cards, smooth page transitions, skeleton shimmer loading
3. **Information Density**: Dashboard cards with clear hierarchy — number → label → trend
4. **Color-Coded Urgency**: Critical=`#ef4444`, High=`#f97316`, Medium=`#3b82f6`, Low=`#6b7280`
5. **Typography**: Inter for body text, Outfit for headings — clean and modern
6. **Accessibility**: Proper focus states, ARIA labels on interactive elements, sufficient contrast ratios

/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Placeholder Pages
   Minimal page stubs for routes that will be fully built in later modules.
   Each page is a simple centered placeholder with the page name.
   ═══════════════════════════════════════════════════════════════════════ */

export function PlaceholderPage({ title, subtitle }) {
  return (
    <div className="page-container">
      <div className="empty-state">
        <div className="empty-state-icon">🚧</div>
        <h1 className="empty-state-title">{title}</h1>
        <p className="text-muted">{subtitle || 'This page will be built in an upcoming module.'}</p>
      </div>
    </div>
  );
}


// ── MSME placeholders ───────────────────────────────────────────────────
export function AlertInboxPage() {
  return <PlaceholderPage title="Alert Inbox" subtitle="Coming in Module F-34" />;
}
export function AlertDetailPage() {
  return <PlaceholderPage title="Alert Detail" subtitle="Coming in Module F-35" />;
}
export function CalendarPage() {
  return <PlaceholderPage title="Compliance Calendar" subtitle="Coming in Module F-36" />;
}
export function ProfileSettingsPage() {
  return <PlaceholderPage title="Profile Settings" subtitle="Coming in Module F-37" />;
}


// ── CA placeholders ─────────────────────────────────────────────────────
export function CADashboardPage() {
  return <PlaceholderPage title="CA Dashboard" subtitle="Coming in Module F-38" />;
}
export function ClientPortfolioPage() {
  return <PlaceholderPage title="Client Portfolio" subtitle="Coming in Module F-39" />;
}
export function DocumentReviewPage() {
  return <PlaceholderPage title="Document Review" subtitle="Coming in Module F-40" />;
}

// ── Admin placeholders ──────────────────────────────────────────────────
export function ScraperHealthPage() {
  return <PlaceholderPage title="Scraper Health" subtitle="Coming in Module F-41" />;
}
export function ScraperRunsPage() {
  return <PlaceholderPage title="Scraper Runs" subtitle="Coming in Module F-42" />;
}
export function UserManagementPage() {
  return <PlaceholderPage title="User Management" subtitle="Coming in Module F-43" />;
}

// ── Error pages ─────────────────────────────────────────────────────────
export function NotFoundPage() {
  return <PlaceholderPage title="404 — Not Found" subtitle="The page you're looking for doesn't exist." />;
}
export function UnauthorizedPage() {
  return <PlaceholderPage title="403 — Unauthorized" subtitle="You don't have permission to access this page." />;
}

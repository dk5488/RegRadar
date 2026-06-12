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






// ── Error pages ─────────────────────────────────────────────────────────
export function NotFoundPage() {
  return <PlaceholderPage title="404 — Not Found" subtitle="The page you're looking for doesn't exist." />;
}
export function UnauthorizedPage() {
  return <PlaceholderPage title="403 — Unauthorized" subtitle="You don't have permission to access this page." />;
}

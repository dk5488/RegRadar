import { useState } from 'react';
import './AdminStyles.css';

// ── Mock Health Data ──────────────────────────────────────────────────
const MOCK_SCRAPERS = [
  { id: 'S-01', name: 'MCA Registry', status: 'online', lastRun: '10 mins ago', successRate: '99.8%', wfaBlocks: 0 },
  { id: 'S-02', name: 'CBIC Notifications', status: 'online', lastRun: '1 hour ago', successRate: '100%', wfaBlocks: 0 },
  { id: 'S-03', name: 'RBI Directives', status: 'warning', lastRun: '2 hours ago', successRate: '94.2%', wfaBlocks: 12 },
  { id: 'S-04', name: 'EPFO Circulars', status: 'online', lastRun: '5 mins ago', successRate: '98.5%', wfaBlocks: 2 },
  { id: 'S-05', name: 'ESIC Updates', status: 'offline', lastRun: '1 day ago', successRate: '0.0%', wfaBlocks: 45 },
  { id: 'S-06', name: 'FSSAI Standards', status: 'online', lastRun: '30 mins ago', successRate: '100%', wfaBlocks: 0 },
];

export function ScraperHealthPage() {
  const [scrapers] = useState(MOCK_SCRAPERS);

  return (
    <div className="admin-page">
      <div className="admin-header">
        <div>
          <h1 className="admin-title">Scraper Health</h1>
          <p className="admin-subtitle">Real-time status of regulatory ingestion engines and WAF bypass metrics.</p>
        </div>
        <button className="btn btn-primary" onClick={() => window.location.reload()}>
          ↻ Refresh Status
        </button>
      </div>

      <div className="health-grid">
        {scrapers.map(scraper => (
          <div key={scraper.id} className="health-card">
            <div className="health-card-header">
              <span className="scraper-name">{scraper.name}</span>
              <div className={`status-dot ${scraper.status}`} title={`Status: ${scraper.status}`}></div>
            </div>
            
            <div className="health-metrics">
              <div className="metric-row">
                <span>Last Sync:</span>
                <span className="metric-value">{scraper.lastRun}</span>
              </div>
              <div className="metric-row">
                <span>Success Rate (24h):</span>
                <span className="metric-value" style={{ color: scraper.successRate === '100%' ? 'var(--color-success-500)' : 'inherit' }}>
                  {scraper.successRate}
                </span>
              </div>
              <div className="metric-row">
                <span>WAF Blocks Detected:</span>
                <span className="metric-value" style={{ color: scraper.wfaBlocks > 10 ? 'var(--color-error-500)' : 'inherit' }}>
                  {scraper.wfaBlocks}
                </span>
              </div>
            </div>

            {scraper.status === 'offline' && (
              <div style={{ marginTop: 'var(--space-4)' }}>
                <button className="btn btn-secondary" style={{ width: '100%', fontSize: '12px' }}>
                  Restart Engine
                </button>
              </div>
            )}
            
          </div>
        ))}
      </div>
    </div>
  );
}

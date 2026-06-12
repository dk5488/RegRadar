import { Link } from 'react-router-dom';
import './CAStyles.css';

// ── Mock Data ─────────────────────────────────────────────────────────
const STATS = {
  totalClients: 42,
  pendingReviews: 15,
  criticalAlerts: 3,
};

const PENDING_REVIEWS = [
  { id: 'DOC-1055', title: 'Revised GST Audit Rules', client: 'Acme Corp', date: '2026-06-12' },
  { id: 'DOC-1056', title: 'EPFO Contribution Update', client: 'TechFlow Solutions', date: '2026-06-11' },
  { id: 'DOC-1057', title: 'Annual Safety Inspection', client: 'Prime Manufacturing', date: '2026-06-10' },
];

export function CADashboardPage() {
  return (
    <div className="ca-page">
      <div className="ca-header">
        <h1 className="ca-title">CA Firm Dashboard</h1>
        <p className="ca-subtitle">Overview of your client portfolio and pending regulatory reviews.</p>
      </div>

      {/* Stats Grid */}
      <div className="ca-stats-grid">
        <div className="ca-stat-card primary">
          <div className="ca-stat-header">
            <span>Total Clients Managed</span>
            <span style={{ fontSize: '1.2rem' }}>🏢</span>
          </div>
          <div className="ca-stat-value">{STATS.totalClients}</div>
        </div>
        
        <div className="ca-stat-card warning">
          <div className="ca-stat-header">
            <span>Pending Document Reviews</span>
            <span style={{ fontSize: '1.2rem' }}>📄</span>
          </div>
          <div className="ca-stat-value">{STATS.pendingReviews}</div>
        </div>
        
        <div className="ca-stat-card success">
          <div className="ca-stat-header">
            <span>Actioned This Week</span>
            <span style={{ fontSize: '1.2rem' }}>✅</span>
          </div>
          <div className="ca-stat-value">28</div>
        </div>
      </div>

      {/* Quick Access: Pending Reviews */}
      <div className="ca-section">
        <div className="ca-section-header">
          <h2 className="ca-section-title">Pending Reviews (Requires Attention)</h2>
          <Link to="/ca/review" className="btn btn-secondary">View All Pipeline</Link>
        </div>
        
        <div className="ca-table-wrapper">
          <table className="ca-table">
            <thead>
              <tr>
                <th>Document ID</th>
                <th>Title</th>
                <th>Target Client</th>
                <th>Ingested Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {PENDING_REVIEWS.map(doc => (
                <tr key={doc.id}>
                  <td style={{ fontFamily: 'var(--font-mono)', fontSize: '12px' }}>{doc.id}</td>
                  <td style={{ fontWeight: '500' }}>{doc.title}</td>
                  <td>{doc.client}</td>
                  <td>{doc.date}</td>
                  <td>
                    <Link to={`/ca/review?doc=${doc.id}`} className="btn btn-secondary" style={{ padding: '4px 12px', fontSize: '12px' }}>
                      Review
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Quick Access: Client Health */}
      <div className="ca-section">
        <div className="ca-section-header">
          <h2 className="ca-section-title">Client Portfolio Health</h2>
          <Link to="/ca/clients" className="btn btn-secondary">Manage Clients</Link>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: 'var(--text-sm)', marginBottom: 'var(--space-4)' }}>
          3 clients have pending critical compliance deadlines this week.
        </p>
        <div className="ca-table-wrapper">
          <table className="ca-table">
            <thead>
              <tr>
                <th>Client Name</th>
                <th>Critical Pending</th>
                <th>Last Login</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><div className="client-name">Acme Corp</div><div className="client-industry">Manufacturing</div></td>
                <td style={{ color: 'var(--color-error-500)', fontWeight: 'bold' }}>2 Alerts</td>
                <td>Today, 09:41 AM</td>
                <td><span className="status-badge critical">Attention</span></td>
              </tr>
              <tr>
                <td><div className="client-name">TechFlow Solutions</div><div className="client-industry">IT/Software</div></td>
                <td>0 Alerts</td>
                <td>Yesterday</td>
                <td><span className="status-badge healthy">Healthy</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}

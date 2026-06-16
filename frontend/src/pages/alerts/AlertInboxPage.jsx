import { useState, useEffect } from 'react';
import { SEO } from '../../components/common/SEO';
import { Link } from 'react-router-dom';
import { documentService } from '../../services/documentService';
import './Alerts.css';

// ── Fallback Mock Data for Premium UI Demo ─────────────────────────────
const MOCK_ALERTS = [
  {
    id: 'DOC-1029',
    title: 'Revised GST Filing Deadlines for Manufacturing Sector',
    authority: 'CBIC',
    published_date: '2026-06-10',
    urgency: 'critical',
    summary: 'The Central Board of Indirect Taxes and Customs has issued a notification revising the GSTR-3B filing deadlines. Entities in the manufacturing sector must file by the 15th of the subsequent month to avoid compounding penalties.',
  },
  {
    id: 'DOC-1028',
    title: 'New EPF Contribution Guidelines for Contract Workers',
    authority: 'EPFO',
    published_date: '2026-06-08',
    urgency: 'high',
    summary: 'Employers are now required to maintain separate EPF ledgers for contract workers. The employer contribution threshold has been adjusted to account for recent minimum wage hikes in specific states.',
  },
  {
    id: 'DOC-1027',
    title: 'Mandatory Udyam Registration Renewal Notice',
    authority: 'Ministry of MSME',
    published_date: '2026-06-05',
    urgency: 'medium',
    summary: 'All registered MSMEs must renew their Udyam certificates within the next 60 days. Failure to do so will result in the suspension of subsidized loan eligibility and priority sector lending benefits.',
  },
  {
    id: 'DOC-1026',
    title: 'Annual Return on Foreign Liabilities and Assets (FLA)',
    authority: 'Reserve Bank of India',
    published_date: '2026-06-01',
    urgency: 'low',
    summary: 'The RBI has opened the portal for filing the Annual Return on FLA for the financial year ending March 2026. Companies that have received FDI or made ODI must comply by July 15.',
  }
];

export function AlertInboxPage() {
  const [alerts, setAlerts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [urgencyFilter, setUrgencyFilter] = useState('all');

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await documentService.list();
        // If API returns empty, use mock data to showcase the UI
        if (response.data && response.data.length > 0) {
          setAlerts(response.data);
        } else {
          setAlerts(MOCK_ALERTS);
        }
      } catch (error) {
        console.error('Failed to fetch alerts', error);
        setAlerts(MOCK_ALERTS);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  const filteredAlerts = alerts.filter(alert => {
    const matchesSearch = alert.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          alert.authority.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesUrgency = urgencyFilter === 'all' || alert.urgency === urgencyFilter;
    return matchesSearch && matchesUrgency;
  });

  const stats = {
    total: alerts.length,
    critical: alerts.filter(a => a.urgency === 'critical').length,
    high: alerts.filter(a => a.urgency === 'high').length,
  };

  return (
    <div className="alerts-page">
      <SEO title="Alert Inbox" description="Review your latest MSME compliance alerts." />
      <div className="page-header">
        <div>
          <h1 className="page-title">Regulatory Alerts</h1>
          <p className="page-subtitle">Stay compliant with the latest regulatory changes tailored for your business.</p>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-icon total">📋</div>
          <div className="stat-content">
            <span className="stat-value">{stats.total}</span>
            <span className="stat-label">Total Alerts</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon critical">⚠️</div>
          <div className="stat-content">
            <span className="stat-value">{stats.critical}</span>
            <span className="stat-label">Critical Actions</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon action">⚡</div>
          <div className="stat-content">
            <span className="stat-value">{stats.high}</span>
            <span className="stat-label">High Priority</span>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="filter-bar">
        <input 
          type="text" 
          className="search-input" 
          placeholder="Search by title or authority..." 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <select 
          className="filter-select"
          value={urgencyFilter}
          onChange={(e) => setUrgencyFilter(e.target.value)}
        >
          <option value="all">All Urgencies</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>

      {/* Alert List */}
      <div className="alert-list">
        {isLoading ? (
          <div style={{ textAlign: 'center', padding: 'var(--space-8)' }}>Loading alerts...</div>
        ) : filteredAlerts.length === 0 ? (
          <div style={{ textAlign: 'center', padding: 'var(--space-8)', color: 'var(--text-muted)' }}>
            No alerts found matching your criteria.
          </div>
        ) : (
          filteredAlerts.map(alert => (
            <Link to={`/alerts/${alert.id}`} key={alert.id} className="alert-card">
              <div className={`alert-card-indicator ${alert.urgency}`}></div>
              <div className="alert-card-content">
                <div className="alert-meta">
                  <span className={`alert-badge ${alert.urgency}`}>{alert.urgency}</span>
                  <span>{alert.authority}</span>
                  <span>•</span>
                  <span>{new Date(alert.published_date).toLocaleDateString()}</span>
                </div>
                <h3 className="alert-title">{alert.title}</h3>
                <p className="alert-summary">{alert.summary}</p>
              </div>
            </Link>
          ))
        )}
      </div>
    </div>
  );
}

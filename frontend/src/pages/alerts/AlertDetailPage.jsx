import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { documentService } from '../../services/documentService';
import './Alerts.css';

// ── Fallback Mock Data for Premium UI Demo ─────────────────────────────
const MOCK_ALERT_DETAIL = {
  id: 'DOC-1029',
  title: 'Revised GST Filing Deadlines for Manufacturing Sector',
  authority: 'Central Board of Indirect Taxes and Customs (CBIC)',
  published_date: '2026-06-10',
  urgency: 'critical',
  original_url: 'https://cbic.gov.in/htdocs-cbec/gst/notification-01-2026',
  ai_summary: `The Central Board of Indirect Taxes and Customs has issued a notification revising the GSTR-3B filing deadlines specifically for the manufacturing sector. 
  
This change aims to streamline the tax collection process and reduce compliance burdens for MSMEs. Entities must now file by the 15th of the subsequent month instead of the 20th.`,
  actions: [
    { id: 1, text: 'Update accounting software to reflect the new 15th of the month deadline.', completed: false },
    { id: 2, text: 'Inform the finance team to process GSTR-3B data 5 days earlier.', completed: false },
    { id: 3, text: 'Review penalty clauses for late filing under the new regime.', completed: false }
  ],
  applicability: 'This regulation applies to your business because your profile lists "Manufacturing" as your primary industry sector and you are registered under GST.'
};

export function AlertDetailPage() {
  const { alertId } = useParams();
  const [alert, setAlert] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [actions, setActions] = useState([]);

  useEffect(() => {
    const fetchAlertDetail = async () => {
      try {
        const response = await documentService.getById(alertId);
        if (response.data) {
          setAlert(response.data);
          setActions(response.data.actions || []);
        } else {
          setAlert({ ...MOCK_ALERT_DETAIL, id: alertId });
          setActions(MOCK_ALERT_DETAIL.actions);
        }
      } catch (error) {
        console.error('Failed to fetch alert details', error);
        setAlert({ ...MOCK_ALERT_DETAIL, id: alertId });
        setActions(MOCK_ALERT_DETAIL.actions);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAlertDetail();
  }, [alertId]);

  const toggleAction = (actionId) => {
    setActions(actions.map(action => 
      action.id === actionId ? { ...action, completed: !action.completed } : action
    ));
  };

  if (isLoading) {
    return <div className="alerts-page" style={{ textAlign: 'center', padding: 'var(--space-10)' }}>Loading document details...</div>;
  }

  if (!alert) {
    return <div className="alerts-page">Alert not found.</div>;
  }

  return (
    <div className="alerts-page">
      <Link to="/alerts" className="back-link">
        <span>←</span> Back to Inbox
      </Link>

      <div className="detail-header">
        <h1 className="detail-title">{alert.title}</h1>
        <div className="detail-meta-row">
          <span className={`alert-badge ${alert.urgency}`}>{alert.urgency}</span>
          <div className="detail-meta-item">
            <span style={{ opacity: 0.7 }}>Authority:</span> {alert.authority}
          </div>
          <div className="detail-meta-item">
            <span style={{ opacity: 0.7 }}>Date:</span> {new Date(alert.published_date).toLocaleDateString()}
          </div>
          <div className="detail-meta-item">
            <span style={{ opacity: 0.7 }}>ID:</span> {alert.id}
          </div>
        </div>
      </div>

      {/* AI Summary Section */}
      <div className="ai-summary-card">
        <div className="ai-header">
          <span className="ai-icon">✨</span>
          <h2 className="ai-title">AI Compliance Summary</h2>
        </div>
        <div className="ai-content">
          {alert.ai_summary.split('\n\n').map((paragraph, idx) => (
            <p key={idx}>{paragraph}</p>
          ))}
        </div>
      </div>

      {/* Required Actions */}
      {actions && actions.length > 0 && (
        <div className="detail-section">
          <h3 className="section-title">Required Actions</h3>
          <ul className="action-list">
            {actions.map(action => (
              <li key={action.id} className="action-item">
                <input 
                  type="checkbox" 
                  className="action-checkbox" 
                  checked={action.completed}
                  onChange={() => toggleAction(action.id)}
                />
                <span className="action-text" style={{ textDecoration: action.completed ? 'line-through' : 'none', opacity: action.completed ? 0.6 : 1 }}>
                  {action.text}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Applicability reasoning */}
      <div className="detail-section">
        <h3 className="section-title">Why this applies to you</h3>
        <p className="ai-content">{alert.applicability}</p>
      </div>

      {/* Original Document Link */}
      <div style={{ marginTop: 'var(--space-8)' }}>
        <a 
          href={alert.original_url} 
          target="_blank" 
          rel="noopener noreferrer" 
          className="doc-link-btn"
        >
          View Original Notification
        </a>
      </div>
    </div>
  );
}

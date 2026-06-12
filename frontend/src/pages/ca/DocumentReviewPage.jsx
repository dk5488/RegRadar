import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import './CAStyles.css';

const MOCK_DOC = {
  id: 'DOC-1055',
  title: 'Revised GST Audit Rules',
  authority: 'CBIC',
  date: '2026-06-12',
  client: 'Acme Corp',
  urgency: 'critical',
  aiSummary: 'The CBIC has revised the GST Audit turnover threshold and filing requirements. Entities with turnover exceeding ₹5 Cr must now file a reconciliation statement electronically.',
  applicabilityReasoning: 'Client "Acme Corp" has reported a turnover of ₹6.2 Cr in the last financial year and operates in the Manufacturing sector, triggering this audit requirement.',
  originalActions: [
    { id: 1, text: 'Prepare GSTR-9C reconciliation statement.' },
    { id: 2, text: 'Submit audited financials before the revised October 31st deadline.' }
  ]
};

export function DocumentReviewPage() {
  const [searchParams] = useSearchParams();
  const docId = searchParams.get('doc');
  const navigate = useNavigate();
  
  const [doc, setDoc] = useState(null);
  const [editedSummary, setEditedSummary] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    // In a real app, fetch the document based on docId
    if (docId) {
      setDoc(MOCK_DOC);
      setEditedSummary(MOCK_DOC.aiSummary);
    } else {
      // If no doc is passed, just load the mock anyway for demo
      setDoc(MOCK_DOC);
      setEditedSummary(MOCK_DOC.aiSummary);
    }
  }, [docId]);

  const handleApprove = async () => {
    setIsSubmitting(true);
    await new Promise(res => setTimeout(res, 800));
    setIsSubmitting(false);
    navigate('/ca/dashboard');
  };

  const handleReject = async () => {
    setIsSubmitting(true);
    await new Promise(res => setTimeout(res, 500));
    setIsSubmitting(false);
    navigate('/ca/dashboard');
  };

  if (!doc) return <div className="ca-page">Loading document...</div>;

  return (
    <div className="ca-page">
      <div className="ca-header">
        <h1 className="ca-title">Review Regulatory Alert</h1>
        <p className="ca-subtitle">Review and refine the AI-generated analysis before dispatching to the client.</p>
      </div>

      <div className="review-layout">
        
        {/* Document Details (Left) */}
        <div className="review-doc-card">
          <h2 className="ca-section-title" style={{ marginBottom: 'var(--space-4)' }}>{doc.title}</h2>
          
          <div className="review-doc-meta">
            <div><span style={{ opacity: 0.7 }}>Target Client:</span> <strong style={{ color: 'var(--text-primary)' }}>{doc.client}</strong></div>
            <div><span style={{ opacity: 0.7 }}>Authority:</span> {doc.authority}</div>
            <div><span style={{ opacity: 0.7 }}>Date:</span> {doc.date}</div>
          </div>

          <div style={{ marginBottom: 'var(--space-6)' }}>
            <h3 style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 'var(--space-2)' }}>
              Why AI Flagged This
            </h3>
            <div style={{ padding: 'var(--space-4)', background: 'rgba(99, 102, 241, 0.05)', border: '1px solid rgba(99, 102, 241, 0.1)', borderRadius: 'var(--radius-lg)', color: 'var(--text-secondary)', fontSize: 'var(--text-sm)' }}>
              {doc.applicabilityReasoning}
            </div>
          </div>

          <div>
            <h3 style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 'var(--space-2)' }}>
              Suggested Actions
            </h3>
            <ul style={{ margin: 0, paddingLeft: 'var(--space-4)', color: 'var(--text-primary)', fontSize: 'var(--text-sm)', lineHeight: '1.6' }}>
              {doc.originalActions.map(action => (
                <li key={action.id} style={{ marginBottom: 'var(--space-2)' }}>{action.text}</li>
              ))}
            </ul>
          </div>
        </div>

        {/* Action Panel (Right) */}
        <div className="review-action-panel">
          <h3 className="ca-section-title" style={{ marginBottom: 'var(--space-5)' }}>CA Review Actions</h3>
          
          <div className="review-input-group">
            <label style={{ display: 'block', fontSize: 'var(--text-sm)', fontWeight: 'var(--font-medium)', color: 'var(--text-secondary)', marginBottom: 'var(--space-2)' }}>
              Edit AI Summary (Client-Facing)
            </label>
            <textarea 
              className="review-textarea"
              value={editedSummary}
              onChange={(e) => setEditedSummary(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', gap: 'var(--space-3)', flexDirection: 'column' }}>
            <button 
              className="btn btn-approve" 
              onClick={handleApprove}
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Processing...' : 'Approve & Dispatch to Client'}
            </button>
            <button 
              className="btn btn-reject" 
              onClick={handleReject}
              disabled={isSubmitting}
            >
              Reject (Does not apply)
            </button>
          </div>
          
          <p style={{ marginTop: 'var(--space-4)', fontSize: '12px', color: 'var(--text-muted)', textAlign: 'center' }}>
            Approving this alert will immediately notify the client via their preferred channels.
          </p>
        </div>

      </div>
    </div>
  );
}

import { useState, useMemo } from 'react';
import './Calendar.css';

// ── Mock Events Data ──────────────────────────────────────────────────
const MOCK_EVENTS = [
  {
    id: 1,
    title: 'GSTR-3B Monthly Return Filing',
    authority: 'CBIC',
    date: '2026-07-15',
    urgency: 'critical',
    status: 'pending',
  },
  {
    id: 2,
    title: 'EPF Contribution Deposit',
    authority: 'EPFO',
    date: '2026-07-15',
    urgency: 'high',
    status: 'pending',
  },
  {
    id: 3,
    title: 'Advance Tax Payment (Q2)',
    authority: 'Income Tax Dept',
    date: '2026-09-15',
    urgency: 'critical',
    status: 'pending',
  },
  {
    id: 4,
    title: 'Annual Return on FLA',
    authority: 'RBI',
    date: '2026-07-15',
    urgency: 'medium',
    status: 'completed',
  },
  {
    id: 5,
    title: 'ESIC Monthly Contribution',
    authority: 'ESIC',
    date: '2026-07-15',
    urgency: 'high',
    status: 'pending',
  },
  {
    id: 6,
    title: 'FSSAI License Renewal',
    authority: 'FSSAI',
    date: '2026-08-10',
    urgency: 'critical',
    status: 'pending',
  }
];

export function CalendarPage() {
  const [events] = useState(MOCK_EVENTS);

  // Group events by month-year
  const groupedEvents = useMemo(() => {
    const groups = {};
    
    // Sort events by date
    const sortedEvents = [...events].sort((a, b) => new Date(a.date) - new Date(b.date));

    sortedEvents.forEach(event => {
      const d = new Date(event.date);
      const monthYear = d.toLocaleString('default', { month: 'long', year: 'numeric' });
      
      if (!groups[monthYear]) {
        groups[monthYear] = [];
      }
      groups[monthYear].push(event);
    });

    return groups;
  }, [events]);

  const stats = useMemo(() => {
    return {
      total: events.length,
      pending: events.filter(e => e.status === 'pending').length,
      completed: events.filter(e => e.status === 'completed').length,
      critical: events.filter(e => e.urgency === 'critical' && e.status === 'pending').length,
    };
  }, [events]);

  const getDay = (dateString) => {
    return new Date(dateString).getDate().toString().padStart(2, '0');
  };

  const getMonthShort = (dateString) => {
    return new Date(dateString).toLocaleString('default', { month: 'short' });
  };

  return (
    <div className="calendar-page">
      <div className="calendar-header">
        <div>
          <h1 className="calendar-title">Compliance Calendar</h1>
          <p className="calendar-subtitle">Track your upcoming regulatory deadlines and filings.</p>
        </div>
      </div>

      <div className="calendar-layout">
        {/* Timeline View */}
        <div className="timeline-container">
          {Object.entries(groupedEvents).map(([monthYear, monthEvents]) => (
            <div key={monthYear} className="month-group">
              <h2 className="month-title">{monthYear}</h2>
              
              <div className="timeline-list">
                {monthEvents.map(event => (
                  <div key={event.id} className={`timeline-item ${event.urgency}`}>
                    <div className="date-box">
                      <span className="date-day">{getDay(event.date)}</span>
                      <span className="date-month">{getMonthShort(event.date)}</span>
                    </div>
                    
                    <div className="event-details">
                      <h3 className="event-title">{event.title}</h3>
                      <div className="event-authority">{event.authority}</div>
                      <div className="event-actions">
                        <span className={`event-status ${event.status}`}>
                          {event.status === 'completed' ? '✓ Completed' : 'Pending'}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Sidebar */}
        <div className="calendar-sidebar">
          <div className="sidebar-card">
            <h3 className="sidebar-title">Summary</h3>
            <div className="summary-list">
              <div className="summary-item">
                <span>Total Deadlines</span>
                <span className="summary-count">{stats.total}</span>
              </div>
              <div className="summary-item">
                <span>Pending</span>
                <span className="summary-count" style={{ color: 'var(--color-warning-500)' }}>{stats.pending}</span>
              </div>
              <div className="summary-item">
                <span>Completed</span>
                <span className="summary-count" style={{ color: 'var(--color-success-600)' }}>{stats.completed}</span>
              </div>
              <div className="summary-item" style={{ marginTop: 'var(--space-2)', paddingTop: 'var(--space-2)', borderTop: '1px solid var(--border-secondary)' }}>
                <span>Critical (Pending)</span>
                <span className="summary-count" style={{ color: 'var(--color-error-500)', borderColor: 'var(--color-error-500)' }}>{stats.critical}</span>
              </div>
            </div>
          </div>
          
          <div className="sidebar-card" style={{ background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(6, 182, 212, 0.1))', borderColor: 'rgba(99, 102, 241, 0.2)' }}>
            <h3 className="sidebar-title" style={{ borderBottomColor: 'rgba(99, 102, 241, 0.2)' }}>Sync to Calendar</h3>
            <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginBottom: 'var(--space-4)' }}>
              Never miss a deadline. Sync these compliance dates directly to your Google or Outlook calendar.
            </p>
            <button className="btn btn-primary" style={{ width: '100%' }}>Connect Calendar</button>
          </div>
        </div>
      </div>
    </div>
  );
}

import { useState } from 'react';
import './CAStyles.css';

// ── Mock Data ─────────────────────────────────────────────────────────
const MOCK_CLIENTS = [
  { id: 'CLI-001', name: 'Acme Corp', industry: 'Manufacturing', state: 'Maharashtra', alerts: 2, status: 'Attention' },
  { id: 'CLI-002', name: 'TechFlow Solutions', industry: 'IT/Software Services', state: 'Karnataka', alerts: 0, status: 'Healthy' },
  { id: 'CLI-003', name: 'Prime Manufacturing', industry: 'Manufacturing', state: 'Gujarat', alerts: 1, status: 'Attention' },
  { id: 'CLI-004', name: 'Global Logistics', industry: 'Logistics/Transport', state: 'Delhi', alerts: 0, status: 'Healthy' },
  { id: 'CLI-005', name: 'Sunrise Healthcare', industry: 'Healthcare/Pharma', state: 'Tamil Nadu', alerts: 0, status: 'Healthy' },
];

export function ClientPortfolioPage() {
  const [searchTerm, setSearchTerm] = useState('');
  
  const filteredClients = MOCK_CLIENTS.filter(client => 
    client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.industry.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="ca-page">
      <div className="ca-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
        <div>
          <h1 className="ca-title">Client Portfolio</h1>
          <p className="ca-subtitle">Manage your MSME clients and view their compliance health.</p>
        </div>
        <button className="btn btn-primary">+ Invite Client</button>
      </div>

      <div className="ca-section">
        <div style={{ marginBottom: 'var(--space-6)' }}>
          <input 
            type="text" 
            placeholder="Search clients by name or industry..." 
            className="form-input"
            style={{ maxWidth: '400px' }}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="ca-table-wrapper">
          <table className="ca-table">
            <thead>
              <tr>
                <th>Client Name</th>
                <th>Industry</th>
                <th>State</th>
                <th>Active Alerts</th>
                <th>Health Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredClients.map(client => (
                <tr key={client.id}>
                  <td data-label="Client Name">
                    <div className="client-name">{client.name}</div>
                    <div className="client-industry" style={{ fontFamily: 'var(--font-mono)' }}>{client.id}</div>
                  </td>
                  <td data-label="Industry">{client.industry}</td>
                  <td data-label="State">{client.state}</td>
                  <td data-label="Active Alerts">
                    <span style={{ color: client.alerts > 0 ? 'var(--color-error-500)' : 'inherit', fontWeight: client.alerts > 0 ? 'bold' : 'normal' }}>
                      {client.alerts}
                    </span>
                  </td>
                  <td data-label="Health Status">
                    <span className={`status-badge ${client.status.toLowerCase()}`}>
                      {client.status}
                    </span>
                  </td>
                  <td data-label="Action">
                    <button className="btn btn-secondary" style={{ padding: '4px 12px', fontSize: '12px' }}>
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
              
              {filteredClients.length === 0 && (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', padding: 'var(--space-8)', color: 'var(--text-muted)' }}>
                    No clients found matching your search.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

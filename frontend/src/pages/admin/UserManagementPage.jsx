import { useState } from 'react';
import './AdminStyles.css';

const MOCK_USERS = [
  { id: 'USR-001', name: 'Admin User', email: 'admin@regradar.com', role: 'admin', status: 'Active', lastLogin: 'Today, 10:00 AM' },
  { id: 'USR-002', name: 'John CA', email: 'john@cahub.com', role: 'ca_firm_admin', status: 'Active', lastLogin: 'Today, 09:15 AM' },
  { id: 'USR-003', name: 'Acme Corp', email: 'compliance@acmecorp.com', role: 'msme_owner', status: 'Active', lastLogin: 'Yesterday' },
  { id: 'USR-004', name: 'Inactive User', email: 'old@company.com', role: 'msme_owner', status: 'Disabled', lastLogin: '2 months ago' },
];

export function UserManagementPage() {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredUsers = MOCK_USERS.filter(u => 
    u.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
    u.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="admin-page">
      <div className="admin-header">
        <div>
          <h1 className="admin-title">User Management</h1>
          <p className="admin-subtitle">Manage user roles, permissions, and account statuses.</p>
        </div>
        <button className="btn btn-primary">Invite User</button>
      </div>

      <div style={{ marginBottom: 'var(--space-6)' }}>
        <input 
          type="text" 
          placeholder="Search users by name or email..." 
          className="form-input"
          style={{ maxWidth: '400px' }}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="admin-table-wrapper">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Last Login</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map(user => (
              <tr key={user.id}>
                <td style={{ fontWeight: '500' }}>{user.name}</td>
                <td style={{ color: 'var(--text-secondary)' }}>{user.email}</td>
                <td>
                  <span className={`role-badge ${user.role.split('_')[0]}`}>
                    {user.role.replace(/_/g, ' ')}
                  </span>
                </td>
                <td style={{ color: 'var(--text-secondary)' }}>{user.lastLogin}</td>
                <td>
                  <span style={{ 
                    color: user.status === 'Active' ? 'var(--color-success-500)' : 'var(--color-error-500)',
                    fontWeight: '500' 
                  }}>
                    {user.status}
                  </span>
                </td>
                <td>
                  <button className="btn btn-secondary" style={{ padding: '4px 12px', fontSize: '12px' }}>
                    Edit
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

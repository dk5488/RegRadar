import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import './Profile.css';

export function ProfileSettingsPage() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('organization');
  const [isSaving, setIsSaving] = useState(false);

  // Form states
  const [orgData, setOrgData] = useState({
    companyName: user?.name || 'Acme Corp',
    email: user?.email || 'admin@acmecorp.com',
    phone: '+91 9876543210',
    address: '123 Tech Park, Mumbai, MH',
  });

  const [notifications, setNotifications] = useState({
    emailAlerts: true,
    criticalOnly: false,
    weeklyDigest: true,
  });

  const handleSave = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    // Simulate API save
    await new Promise(resolve => setTimeout(resolve, 800));
    setIsSaving(false);
  };

  return (
    <div className="profile-page">
      <div className="profile-header">
        <h1 className="profile-title">Settings & Profile</h1>
        <p className="profile-subtitle">Manage your organization details and notification preferences.</p>
      </div>

      <div className="settings-layout">
        {/* Navigation Sidebar */}
        <div className="settings-nav">
          <button 
            className={`nav-item ${activeTab === 'organization' ? 'active' : ''}`}
            onClick={() => setActiveTab('organization')}
          >
            Organization Details
          </button>
          <button 
            className={`nav-item ${activeTab === 'notifications' ? 'active' : ''}`}
            onClick={() => setActiveTab('notifications')}
          >
            Notifications
          </button>
          <button 
            className={`nav-item ${activeTab === 'security' ? 'active' : ''}`}
            onClick={() => setActiveTab('security')}
          >
            Security & Password
          </button>
        </div>

        {/* Content Area */}
        <div className="settings-content">
          
          {activeTab === 'organization' && (
            <div className="settings-card">
              <div className="card-header">
                <h2 className="card-title">Organization Profile</h2>
                <p className="card-subtitle">Update your company's contact and basic information.</p>
              </div>
              <form className="settings-form" onSubmit={handleSave}>
                <div className="form-group">
                  <label className="form-label">Company Name</label>
                  <input 
                    type="text" 
                    className="form-input" 
                    value={orgData.companyName}
                    onChange={(e) => setOrgData({...orgData, companyName: e.target.value})}
                  />
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Contact Email</label>
                    <input 
                      type="email" 
                      className="form-input" 
                      value={orgData.email}
                      onChange={(e) => setOrgData({...orgData, email: e.target.value})}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Phone Number</label>
                    <input 
                      type="text" 
                      className="form-input" 
                      value={orgData.phone}
                      onChange={(e) => setOrgData({...orgData, phone: e.target.value})}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label className="form-label">Registered Address</label>
                  <input 
                    type="text" 
                    className="form-input" 
                    value={orgData.address}
                    onChange={(e) => setOrgData({...orgData, address: e.target.value})}
                  />
                </div>
                <div className="settings-actions">
                  <button type="submit" className="btn btn-primary" disabled={isSaving}>
                    {isSaving ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              </form>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="settings-card">
              <div className="card-header">
                <h2 className="card-title">Notification Preferences</h2>
                <p className="card-subtitle">Choose how and when you want to be alerted about compliance updates.</p>
              </div>
              <div className="settings-form">
                
                <div className="toggle-group">
                  <div className="toggle-info">
                    <span className="toggle-title">Email Alerts</span>
                    <span className="toggle-desc">Receive real-time email notifications for new regulations.</span>
                  </div>
                  <label className="switch">
                    <input 
                      type="checkbox" 
                      checked={notifications.emailAlerts}
                      onChange={(e) => setNotifications({...notifications, emailAlerts: e.target.checked})}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="toggle-group">
                  <div className="toggle-info">
                    <span className="toggle-title">Critical Alerts Only</span>
                    <span className="toggle-desc">Only notify me for high-urgency or critical compliance deadlines.</span>
                  </div>
                  <label className="switch">
                    <input 
                      type="checkbox" 
                      checked={notifications.criticalOnly}
                      onChange={(e) => setNotifications({...notifications, criticalOnly: e.target.checked})}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="toggle-group">
                  <div className="toggle-info">
                    <span className="toggle-title">Weekly Digest</span>
                    <span className="toggle-desc">Get a weekly summary of all regulatory changes every Monday.</span>
                  </div>
                  <label className="switch">
                    <input 
                      type="checkbox" 
                      checked={notifications.weeklyDigest}
                      onChange={(e) => setNotifications({...notifications, weeklyDigest: e.target.checked})}
                    />
                    <span className="slider"></span>
                  </label>
                </div>

                <div className="settings-actions">
                  <button className="btn btn-primary" onClick={handleSave} disabled={isSaving}>
                    {isSaving ? 'Saving...' : 'Save Preferences'}
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="settings-card">
              <div className="card-header">
                <h2 className="card-title">Security & Password</h2>
                <p className="card-subtitle">Manage your password and account security settings.</p>
              </div>
              <form className="settings-form" onSubmit={handleSave}>
                <div className="form-group">
                  <label className="form-label">Current Password</label>
                  <input type="password" className="form-input" placeholder="••••••••" />
                </div>
                <div className="form-group">
                  <label className="form-label">New Password</label>
                  <input type="password" className="form-input" placeholder="Create a new strong password" />
                </div>
                <div className="form-group">
                  <label className="form-label">Confirm New Password</label>
                  <input type="password" className="form-input" placeholder="Confirm your new password" />
                </div>
                <div className="settings-actions">
                  <button type="submit" className="btn btn-primary" disabled={isSaving}>
                    {isSaving ? 'Updating...' : 'Update Password'}
                  </button>
                </div>
              </form>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}

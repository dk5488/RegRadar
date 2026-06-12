import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { USER_ROLES } from '../../utils/constants';
import './Auth.css';

export function RegisterPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState(USER_ROLES.MSME_OWNER);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      await register({ name, email, password, role });
      navigate('/');
    } catch (err) {
      setError(err.message || 'Failed to register. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-page-container">
      {/* Background Orbs */}
      <div className="auth-bg-orb auth-bg-orb-1" style={{ top: '-50px', left: 'auto', right: '-100px' }} />
      <div className="auth-bg-orb auth-bg-orb-2" style={{ bottom: '-100px', right: 'auto', left: '-50px' }} />

      <div className="auth-card">
        <div className="auth-header">
          <Link to="/" style={{ textDecoration: 'none' }}>
            <div className="auth-logo">RegRadar</div>
          </Link>
          <h1 className="auth-title">Create an account</h1>
          <p className="auth-subtitle">Join RegRadar to streamline your compliance</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          
          <div className="form-group">
            <label className="form-label">I am a...</label>
            <div className="role-selector">
              <div 
                className={`role-option ${role === USER_ROLES.MSME_OWNER ? 'active' : ''}`}
                onClick={() => setRole(USER_ROLES.MSME_OWNER)}
              >
                Business Owner
              </div>
              <div 
                className={`role-option ${role === USER_ROLES.CA_FIRM_ADMIN ? 'active' : ''}`}
                onClick={() => setRole(USER_ROLES.CA_FIRM_ADMIN)}
              >
                CA / Professional
              </div>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="name">Full Name or Company</label>
            <div className="form-input-wrapper">
              <input
                id="name"
                type="text"
                className="form-input"
                placeholder="Acme Corp / John Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="email">Email Address</label>
            <div className="form-input-wrapper">
              <input
                id="email"
                type="email"
                className="form-input"
                placeholder="you@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <div className="form-input-wrapper">
              <input
                id="password"
                type="password"
                className="form-input"
                placeholder="Create a strong password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          {error && <div className="form-error">{error}</div>}

          <button type="submit" className="auth-button" disabled={isLoading}>
            {isLoading ? 'Creating account...' : 'Sign up'}
          </button>
        </form>

        <div className="auth-footer">
          Already have an account?{' '}
          <Link to="/login" className="auth-link">
            Sign in
          </Link>
        </div>
      </div>
    </div>
  );
}

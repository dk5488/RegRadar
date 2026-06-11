/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — ProtectedRoute
   Wraps routes that require authentication and optionally checks roles.
   ═══════════════════════════════════════════════════════════════════════ */

import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

/**
 * @param {object} props
 * @param {React.ReactNode} props.children - The route content
 * @param {string[]} [props.allowedRoles] - Optional array of role strings
 */
export default function ProtectedRoute({ children, allowedRoles }) {
  const { isAuthenticated, user, loading } = useAuth();
  const location = useLocation();

  // Still checking auth state
  if (loading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
      }}>
        <div className="spinner spinner-lg" />
      </div>
    );
  }

  // Not authenticated → redirect to login
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Role check (if roles are specified)
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
}

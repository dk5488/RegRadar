/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — withRoleGuard (HOC)
   Higher Order Component for role-based access control.
   ═══════════════════════════════════════════════════════════════════════ */

import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export default function withRoleGuard(WrappedComponent, allowedRoles) {
  return function RoleGuard(props) {
    const { isAuthenticated, user, loading } = useAuth();

    if (loading) {
      return (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
          <div className="spinner spinner-lg" />
        </div>
      );
    }

    if (!isAuthenticated) {
      return <Navigate to="/login" replace />;
    }

    if (allowedRoles && !allowedRoles.includes(user.role)) {
      return <Navigate to="/unauthorized" replace />;
    }

    return <WrappedComponent {...props} />;
  };
}

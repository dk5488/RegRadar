/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Auth Context
   Provides authentication state, login/logout/register actions,
   and role-based access helpers to the entire app.
   ═══════════════════════════════════════════════════════════════════════ */

import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // ── Bootstrap: check for existing token on mount ────────────────────
  useEffect(() => {
    const token = localStorage.getItem('regr_token');
    if (token) {
      authService
        .getMe()
        .then((res) => setUser(res.data))
        .catch(() => {
          localStorage.removeItem('regr_token');
          localStorage.removeItem('regr_user');
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  // ── Login ───────────────────────────────────────────────────────────
  const login = useCallback(async (email, password) => {
    setError(null);
    try {
      const { data } = await authService.login({ email, password });
      localStorage.setItem('regr_token', data.access_token);

      const { data: userData } = await authService.getMe();
      setUser(userData);
      localStorage.setItem('regr_user', JSON.stringify(userData));
      return userData;
    } catch (err) {
      const message = err.response?.data?.detail || 'Login failed';
      setError(message);
      throw err;
    }
  }, []);

  // ── Register ────────────────────────────────────────────────────────
  const register = useCallback(async (userData) => {
    setError(null);
    try {
      const { data } = await authService.register(userData);
      return data;
    } catch (err) {
      const message = err.response?.data?.detail || 'Registration failed';
      setError(message);
      throw err;
    }
  }, []);

  // ── Logout ──────────────────────────────────────────────────────────
  const logout = useCallback(() => {
    localStorage.removeItem('regr_token');
    localStorage.removeItem('regr_user');
    setUser(null);
  }, []);

  // ── Role checks ────────────────────────────────────────────────────
  const isAdmin = user?.role === 'admin';
  const isCA = user?.role === 'ca_firm_admin' || user?.role === 'ca_reviewer';
  const isCAAdmin = user?.role === 'ca_firm_admin';
  const isCAReviewer = user?.role === 'ca_reviewer';
  const isMSME = user?.role === 'msme_owner';
  const isAuthenticated = !!user;

  const value = {
    user,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    isCA,
    isCAAdmin,
    isCAReviewer,
    isMSME,
    login,
    register,
    logout,
    setError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook to access auth context.
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

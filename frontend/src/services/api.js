/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Axios API Client
   Centralized HTTP client with JWT interceptor and error handling.
   ═══════════════════════════════════════════════════════════════════════ */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ── Request interceptor: attach JWT ─────────────────────────────────────
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('regr_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ── Response interceptor: handle 401 / errors ───────────────────────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { status } = error.response;

      if (status === 401) {
        // Token expired or invalid — clear and redirect
        localStorage.removeItem('regr_token');
        localStorage.removeItem('regr_user');
        // Only redirect if not already on auth pages
        if (!window.location.pathname.startsWith('/login') &&
            !window.location.pathname.startsWith('/register')) {
          window.location.href = '/login';
        }
      }
    }

    return Promise.reject(error);
  }
);

export default api;

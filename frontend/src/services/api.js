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

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

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

// ── Response interceptor: handle 401 / refresh logic ────────────────────
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If status is 401 and we haven't already retried this request
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Queue this request and wait for the refresh to complete
        return new Promise(function(resolve, reject) {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token;
          return api(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = localStorage.getItem('regr_refresh_token');
      
      if (!refreshToken) {
        // No refresh token available, force logout
        processQueue(error, null);
        isRefreshing = false;
        localStorage.removeItem('regr_token');
        localStorage.removeItem('regr_user');
        if (!window.location.pathname.startsWith('/login') &&
            !window.location.pathname.startsWith('/register')) {
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }

      try {
        // Placeholder for actual refresh logic when backend supports it
        // const { data } = await axios.post(`${API_BASE_URL}/auth/refresh`, { refresh_token: refreshToken });
        // const newToken = data.access_token;
        // localStorage.setItem('regr_token', newToken);
        
        // For now, simulate a failure since we don't have a real endpoint yet
        throw new Error('Refresh not implemented');

        // api.defaults.headers.common['Authorization'] = 'Bearer ' + newToken;
        // originalRequest.headers['Authorization'] = 'Bearer ' + newToken;
        // processQueue(null, newToken);
        // return api(originalRequest);
      } catch (err) {
        processQueue(err, null);
        localStorage.removeItem('regr_token');
        localStorage.removeItem('regr_refresh_token');
        localStorage.removeItem('regr_user');
        if (!window.location.pathname.startsWith('/login') &&
            !window.location.pathname.startsWith('/register')) {
          window.location.href = '/login';
        }
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;

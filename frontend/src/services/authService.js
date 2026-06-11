/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Auth Service
   API calls for registration, login, and user info.
   ═══════════════════════════════════════════════════════════════════════ */

import api from './api';

export const authService = {
  /**
   * Register a new user account.
   * @param {{ email: string, password: string, full_name: string, phone?: string, role?: string }} data
   */
  register(data) {
    return api.post('/auth/register', data);
  },

  /**
   * Log in and receive a JWT.
   * @param {{ email: string, password: string }} credentials
   */
  login(credentials) {
    return api.post('/auth/login', credentials);
  },

  /**
   * Get the currently authenticated user's profile.
   */
  getMe() {
    return api.get('/auth/me');
  },
};

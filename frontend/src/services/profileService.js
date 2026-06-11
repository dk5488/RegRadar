/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Profile Service
   API calls for MSME business profiles CRUD.
   ═══════════════════════════════════════════════════════════════════════ */

import api from './api';

export const profileService = {
  /**
   * Create a new business profile (onboarding).
   */
  create(data) {
    return api.post('/profiles', data);
  },

  /**
   * List profiles with pagination.
   */
  list(params = {}) {
    return api.get('/profiles', { params });
  },

  /**
   * Get a single profile by ID.
   */
  getById(id) {
    return api.get(`/profiles/${id}`);
  },

  /**
   * Partially update a profile.
   */
  update(id, data) {
    return api.patch(`/profiles/${id}`, data);
  },

  /**
   * Soft-delete (deactivate) a profile.
   */
  deactivate(id) {
    return api.delete(`/profiles/${id}`);
  },
};

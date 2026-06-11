/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Alert Service
   API calls for the user-facing alert inbox.
   ═══════════════════════════════════════════════════════════════════════ */

import api from './api';

export const alertService = {
  /**
   * List alerts with filters and pagination.
   */
  list(params = {}) {
    return api.get('/alerts', { params });
  },

  /**
   * Get a single alert by ID.
   */
  getById(id) {
    return api.get(`/alerts/${id}`);
  },

  /**
   * Acknowledge an alert (noted / done / not_applicable).
   */
  acknowledge(id, data) {
    return api.post(`/alerts/${id}/acknowledge`, data);
  },
};

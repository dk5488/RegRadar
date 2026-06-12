/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Compliance Service
   API calls for compliance items (applicability matrix).
   ═══════════════════════════════════════════════════════════════════════ */

import api from './api';

export const complianceService = {
  /**
   * Create a new compliance item (CA/Admin only).
   */
  create(data) {
    return api.post('/compliance', data);
  },

  /**
   * List compliance items with filters and pagination.
   */
  list(params = {}) {
    return api.get('/compliance', { params });
  },

  /**
   * Get a single compliance item by ID.
   */
  getById(id) {
    return api.get(`/compliance/${id}`);
  },
};

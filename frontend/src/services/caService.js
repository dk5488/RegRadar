/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — CA Dashboard Service
   API calls for CA firm management and dashboard.
   ═══════════════════════════════════════════════════════════════════════ */

import api from './api';

export const caService = {
  /**
   * Register a new CA firm.
   */
  createFirm(data) {
    return api.post('/ca/firms', data);
  },

  /**
   * Get CA firm details.
   */
  getFirm(firmId) {
    return api.get(`/ca/firms/${firmId}`);
  },

  /**
   * Get dashboard summary for a CA firm.
   */
  getDashboard(firmId) {
    return api.get(`/ca/firms/${firmId}/dashboard`);
  },
};

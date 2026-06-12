/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Health Service
   API calls for scraper health monitoring (Admin only).
   ═══════════════════════════════════════════════════════════════════════ */

import api from './api';

export const healthService = {
  /**
   * List health status of all registered sources.
   */
  listSources() {
    return api.get('/health/sources');
  },

  /**
   * List historical scraper runs with pagination.
   */
  listRuns(params = {}) {
    return api.get('/health/runs', { params });
  },
};

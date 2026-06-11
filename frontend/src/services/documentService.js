/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Document Service
   API calls for regulatory documents and CA review workflow.
   ═══════════════════════════════════════════════════════════════════════ */

import api from './api';

export const documentService = {
  /**
   * List documents with filters and pagination.
   */
  list(params = {}) {
    return api.get('/documents', { params });
  },

  /**
   * Get a single document by ID.
   */
  getById(id) {
    return api.get(`/documents/${id}`);
  },

  /**
   * Review a document (approve / edit / reject). CA role required.
   */
  review(id, data) {
    return api.post(`/documents/${id}/review`, data);
  },
};

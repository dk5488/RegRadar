/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Formatters & Helpers
   Shared utility functions for dates, urgency colors, etc.
   ═══════════════════════════════════════════════════════════════════════ */

/**
 * Format an ISO date string into a human-readable format.
 * @param {string} dateStr - ISO date string
 * @param {object} opts - Intl.DateTimeFormat options override
 * @returns {string}
 */
export function formatDate(dateStr, opts = {}) {
  if (!dateStr) return '—';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    ...opts,
  });
}

/**
 * Format a date into relative time ("3 minutes ago", "2 days ago").
 * @param {string} dateStr - ISO date string
 * @returns {string}
 */
export function timeAgo(dateStr) {
  if (!dateStr) return '—';
  const now = new Date();
  const past = new Date(dateStr);
  const diffMs = now - past;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHr = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHr / 24);

  if (diffSec < 60) return 'Just now';
  if (diffMin < 60) return `${diffMin}m ago`;
  if (diffHr < 24) return `${diffHr}h ago`;
  if (diffDay < 7) return `${diffDay}d ago`;
  return formatDate(dateStr);
}

/**
 * Get CSS class name for an urgency level.
 * @param {string} urgency - 'Critical' | 'High' | 'Medium' | 'Low'
 * @returns {string}
 */
export function urgencyBadgeClass(urgency) {
  const map = {
    Critical: 'badge-critical',
    High: 'badge-high',
    Medium: 'badge-medium',
    Low: 'badge-low',
  };
  return map[urgency] || 'badge-low';
}

/**
 * Get CSS class for an alert status.
 * @param {string} status
 * @returns {string}
 */
export function statusBadgeClass(status) {
  const map = {
    pending: 'badge-medium',
    sent: 'badge-info',
    delivered: 'badge-info',
    read: 'badge-success',
    noted: 'badge-success',
    done: 'badge-success',
    not_applicable: 'badge-low',
    failed: 'badge-critical',
  };
  return map[status] || 'badge-low';
}

/**
 * Get confidence color based on score.
 * @param {number} score - 0.0 to 1.0
 * @returns {'green' | 'yellow' | 'red'}
 */
export function confidenceColor(score) {
  if (score == null) return 'low';
  if (score >= 0.8) return 'green';
  if (score >= 0.5) return 'yellow';
  return 'red';
}

/**
 * Truncate text to maxLen characters with ellipsis.
 * @param {string} text
 * @param {number} maxLen
 * @returns {string}
 */
export function truncate(text, maxLen = 100) {
  if (!text) return '';
  if (text.length <= maxLen) return text;
  return text.slice(0, maxLen).trimEnd() + '…';
}

/**
 * Calculate days remaining until a deadline.
 * @param {string} deadlineStr - ISO date string
 * @returns {number|null}
 */
export function daysUntil(deadlineStr) {
  if (!deadlineStr) return null;
  const now = new Date();
  const deadline = new Date(deadlineStr);
  const diffMs = deadline - now;
  return Math.ceil(diffMs / (1000 * 60 * 60 * 24));
}

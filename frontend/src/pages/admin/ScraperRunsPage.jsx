import { useState, useEffect, useRef } from 'react';
import './AdminStyles.css';

// ── Mock Terminal Logs ────────────────────────────────────────────────
const MOCK_LOGS = [
  { time: '10:01:45.123', level: 'info', msg: 'Initializing TaskQueue scheduler...' },
  { time: '10:01:46.002', level: 'info', msg: 'Started scraping sequence for [CBIC]' },
  { time: '10:01:48.334', level: 'info', msg: 'HTTP 200 OK - Fetched https://cbic.gov.in/notifications' },
  { time: '10:01:49.100', level: 'info', msg: 'Parsed 12 raw documents. Deduplicating against DB...' },
  { time: '10:01:50.050', level: 'info', msg: 'Found 1 new document. Extracting metadata...' },
  { time: '10:02:15.890', level: 'warn', msg: 'Rate limit approaching on [RBI] endpoint. Cooling down.' },
  { time: '10:05:00.001', level: 'info', msg: 'Started scraping sequence for [ESIC]' },
  { time: '10:05:05.400', level: 'error', msg: 'HTTP 403 Forbidden - WAF Block detected (Akamai)' },
  { time: '10:05:05.450', level: 'warn', msg: 'Retrying [ESIC] with curl_cffi TLS impersonation...' },
  { time: '10:05:12.110', level: 'error', msg: 'Max retries exceeded for [ESIC]. Marking node offline.' },
];

export function ScraperRunsPage() {
  const [logs, setLogs] = useState([]);
  const terminalRef = useRef(null);

  // Simulate streaming logs
  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      if (i < MOCK_LOGS.length) {
        setLogs(prev => [...prev, MOCK_LOGS[i]]);
        i++;
      } else {
        clearInterval(interval);
      }
    }, 800);

    return () => clearInterval(interval);
  }, []);

  // Auto-scroll terminal
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="admin-page">
      <div className="admin-header">
        <div>
          <h1 className="admin-title">Scraper Run Logs</h1>
          <p className="admin-subtitle">Live terminal output from the ingestion workers.</p>
        </div>
      </div>

      <div className="terminal-container">
        <div className="terminal-header">
          <span className="terminal-title">Worker Process: celery_worker_1</span>
          <div className="terminal-actions">
            <button className="terminal-btn" onClick={() => setLogs([])}>Clear</button>
            <button className="terminal-btn">Download .log</button>
          </div>
        </div>
        <div className="terminal-body" ref={terminalRef}>
          {logs.map((log, idx) => (
            <div key={idx} className="log-line">
              <span className="log-time">[{log.time}]</span>
              <span className={`log-level ${log.level}`}>[{log.level.toUpperCase()}]</span>
              <span className="log-msg">{log.msg}</span>
            </div>
          ))}
          <div className="log-line">
            <span className="log-msg" style={{ opacity: 0.5, animation: 'pulse 1s infinite alternate' }}>_</span>
          </div>
        </div>
      </div>

      <div>
        <h3 style={{ marginBottom: 'var(--space-4)', color: 'var(--text-primary)' }}>Recent Execution History</h3>
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr>
                <th>Run ID</th>
                <th>Target</th>
                <th>Status</th>
                <th>Duration</th>
                <th>Docs Extracted</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style={{ fontFamily: 'var(--font-mono)' }}>job_a1b2c3</td>
                <td>CBIC</td>
                <td><span style={{ color: 'var(--color-success-500)' }}>Success</span></td>
                <td>4.2s</td>
                <td>1</td>
              </tr>
              <tr>
                <td style={{ fontFamily: 'var(--font-mono)' }}>job_x9y8z7</td>
                <td>ESIC</td>
                <td><span style={{ color: 'var(--color-error-500)' }}>Failed</span></td>
                <td>12.1s</td>
                <td>0</td>
              </tr>
              <tr>
                <td style={{ fontFamily: 'var(--font-mono)' }}>job_m5n6o7</td>
                <td>MCA</td>
                <td><span style={{ color: 'var(--color-success-500)' }}>Success</span></td>
                <td>18.5s</td>
                <td>14</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

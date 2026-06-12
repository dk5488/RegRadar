/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Sidebar
   Role-based collapsible side navigation.
   ═══════════════════════════════════════════════════════════════════════ */

import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { USER_ROLES } from '../../utils/constants';
import {
  FiInbox,
  FiCalendar,
  FiSettings,
  FiUsers,
  FiFileText,
  FiActivity,
  FiDatabase,
  FiChevronLeft,
  FiChevronRight,
  FiTarget,
  FiBriefcase
} from 'react-icons/fi';
import './Sidebar.css';

export default function Sidebar() {
  const { user } = useAuth();
  const [isCollapsed, setIsCollapsed] = useState(false);

  // Define navigation links by role
  const getNavLinks = () => {
    if (!user) return [];

    switch (user.role) {
      case USER_ROLES.ADMIN:
        return [
          { to: '/admin/scrapers', icon: FiActivity, label: 'Scraper Health' },
          { to: '/admin/runs', icon: FiDatabase, label: 'Scraper Runs' },
          { to: '/admin/users', icon: FiUsers, label: 'User Management' },
        ];
      case USER_ROLES.CA_FIRM_ADMIN:
      case USER_ROLES.CA_REVIEWER:
        return [
          { to: '/ca/dashboard', icon: FiTarget, label: 'CA Dashboard' },
          { to: '/ca/clients', icon: FiBriefcase, label: 'Client Portfolio' },
          { to: '/ca/review', icon: FiFileText, label: 'Document Review' },
        ];
      case USER_ROLES.MSME_OWNER:
      default:
        return [
          { to: '/alerts', icon: FiInbox, label: 'Alert Inbox' },
          { to: '/calendar', icon: FiCalendar, label: 'Calendar' },
          { to: '/profile', icon: FiSettings, label: 'Profile Settings' },
        ];
    }
  };

  const navLinks = getNavLinks();

  return (
    <aside className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
      {/* ── Logo Area ── */}
      <div className="sidebar-header">
        <div className="logo-container">
          <FiTarget className="logo-icon" />
          {!isCollapsed && <span className="logo-text">RegRadar</span>}
        </div>
      </div>

      {/* ── Navigation Links ── */}
      <nav className="sidebar-nav">
        <ul>
          {navLinks.map((link) => (
            <li key={link.to}>
              <NavLink
                to={link.to}
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                title={isCollapsed ? link.label : undefined}
              >
                <link.icon className="nav-icon" />
                {!isCollapsed && <span className="nav-label">{link.label}</span>}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* ── Collapse Toggle ── */}
      <div className="sidebar-footer">
        <button
          className="collapse-btn"
          onClick={() => setIsCollapsed(!isCollapsed)}
          aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {isCollapsed ? <FiChevronRight /> : <FiChevronLeft />}
          {!isCollapsed && <span>Collapse</span>}
        </button>
      </div>
    </aside>
  );
}

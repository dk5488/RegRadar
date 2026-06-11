/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — Navbar
   Top navigation bar containing user profile, role badge, and theme toggle.
   ═══════════════════════════════════════════════════════════════════════ */

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useTheme } from '../../context/ThemeContext';
import { ROLE_LABELS } from '../../utils/constants';
import { FiSun, FiMoon, FiUser, FiLogOut, FiMenu, FiBell } from 'react-icons/fi';
import './Navbar.css';

export default function Navbar({ onMenuClick }) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  if (!user) return null;

  return (
    <header className="navbar">
      <div className="navbar-left">
        <button className="mobile-menu-btn" onClick={onMenuClick} aria-label="Open menu">
          <FiMenu />
        </button>
      </div>

      <div className="navbar-right">
        {/* Theme Toggle */}
        <button
          className="icon-btn"
          onClick={toggleTheme}
          aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {theme === 'dark' ? <FiSun /> : <FiMoon />}
        </button>

        {/* Notifications (Placeholder) */}
        <button className="icon-btn notification-btn" aria-label="Notifications">
          <FiBell />
          <span className="notification-dot"></span>
        </button>

        {/* User Profile Dropdown */}
        <div className="profile-menu" ref={dropdownRef}>
          <button
            className="profile-btn"
            onClick={() => setShowDropdown(!showDropdown)}
            aria-expanded={showDropdown}
          >
            <div className="avatar">
              {user.full_name.charAt(0).toUpperCase()}
            </div>
            <div className="profile-info">
              <span className="profile-name">{user.full_name}</span>
              <span className="profile-role">{ROLE_LABELS[user.role]}</span>
            </div>
          </button>

          {showDropdown && (
            <div className="dropdown-menu animate-fade-in-up">
              <div className="dropdown-header">
                <p className="dropdown-name">{user.full_name}</p>
                <p className="dropdown-email">{user.email}</p>
              </div>
              <div className="dropdown-divider"></div>
              <button className="dropdown-item">
                <FiUser />
                Profile Settings
              </button>
              <button className="dropdown-item text-danger" onClick={handleLogout}>
                <FiLogOut />
                Sign Out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

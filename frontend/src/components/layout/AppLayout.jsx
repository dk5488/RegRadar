/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — App Layout Shell
   The main layout wrapper for authenticated routes.
   Includes the Sidebar, Navbar, and Outlet for page content.
   ═══════════════════════════════════════════════════════════════════════ */

import { useState, useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import './AppLayout.css';

export default function AppLayout() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  // Close mobile menu when route changes
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  // Lock body scroll when mobile menu is open
  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [mobileMenuOpen]);

  return (
    <div className="app-layout">
      {/* Mobile Overlay */}
      {mobileMenuOpen && (
        <div 
          className="mobile-overlay animate-fade-in" 
          onClick={() => setMobileMenuOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar Wrapper for mobile control */}
      <div className={`sidebar-wrapper ${mobileMenuOpen ? 'mobile-open' : ''}`}>
        <Sidebar />
      </div>

      {/* Main Content Area */}
      <div className="main-content">
        <Navbar onMenuClick={() => setMobileMenuOpen(true)} />
        
        <main className="page-wrapper">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

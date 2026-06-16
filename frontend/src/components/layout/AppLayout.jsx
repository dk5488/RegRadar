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
  const location = useLocation();

  return (
    <div className="app-layout">
      {/* Sidebar Wrapper for mobile control */}
      <div className="sidebar-wrapper">
        <Sidebar />
      </div>

      {/* Main Content Area */}
      <div className="main-content">
        <Navbar />
        
        <main className="page-wrapper">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

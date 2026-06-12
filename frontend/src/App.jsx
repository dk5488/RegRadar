/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — App Root
   React Router setup with role-based route protection.
   ═══════════════════════════════════════════════════════════════════════ */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import ProtectedRoute from './components/common/ProtectedRoute';
import AppLayout from './components/layout/AppLayout';
import { USER_ROLES } from './utils/constants';

// ── Page imports (placeholders for now, replaced module-by-module) ────
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';

import { OnboardingPage } from './pages/onboarding/OnboardingPage';

import { AlertInboxPage } from './pages/alerts/AlertInboxPage';
import { AlertDetailPage } from './pages/alerts/AlertDetailPage';

import { CalendarPage } from './pages/calendar/CalendarPage';
import { ProfileSettingsPage } from './pages/profile/ProfileSettingsPage';

import { CADashboardPage } from './pages/ca/CADashboardPage';
import { ClientPortfolioPage } from './pages/ca/ClientPortfolioPage';
import { DocumentReviewPage } from './pages/ca/DocumentReviewPage';

import { ScraperHealthPage } from './pages/admin/ScraperHealthPage';
import { ScraperRunsPage } from './pages/admin/ScraperRunsPage';
import { UserManagementPage } from './pages/admin/UserManagementPage';

import {
  NotFoundPage,
  UnauthorizedPage,
} from './pages/Placeholders';

// ── Smart redirect based on role ─────────────────────────────────────
function DashboardRedirect() {
  const { user } = useAuth();

  if (!user) return <Navigate to="/login" replace />;

  switch (user.role) {
    case USER_ROLES.ADMIN:
      return <Navigate to="/admin/scrapers" replace />;
    case USER_ROLES.CA_FIRM_ADMIN:
    case USER_ROLES.CA_REVIEWER:
      return <Navigate to="/ca/dashboard" replace />;
    case USER_ROLES.MSME_OWNER:
    default:
      return <Navigate to="/alerts" replace />;
  }
}

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <Routes>
            {/* ── Public Routes ─────────────────────────────────────── */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* ── Authenticated Standalone Routes ───────────────────── */}
            <Route
              path="/onboarding"
              element={
                <ProtectedRoute>
                  <OnboardingPage />
                </ProtectedRoute>
              }
            />

            {/* ── Authenticated Routes with AppLayout ───────────────── */}
            <Route
              element={
                <ProtectedRoute>
                  <AppLayout />
                </ProtectedRoute>
              }
            >
              {/* ── Smart Dashboard Redirect ──────────────────────────── */}
              <Route path="/" element={<DashboardRedirect />} />

              {/* ── MSME Owner Routes ────────────────────────────────── */}
              <Route path="/alerts" element={<AlertInboxPage />} />
              <Route path="/alerts/:alertId" element={<AlertDetailPage />} />
              <Route path="/calendar" element={<CalendarPage />} />
              <Route path="/profile" element={<ProfileSettingsPage />} />

              {/* ── CA Firm Routes ────────────────────────────────────── */}
              <Route
                path="/ca/dashboard"
                element={
                  <ProtectedRoute allowedRoles={[USER_ROLES.CA_FIRM_ADMIN, USER_ROLES.CA_REVIEWER, USER_ROLES.ADMIN]}>
                    <CADashboardPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/ca/clients"
                element={
                  <ProtectedRoute allowedRoles={[USER_ROLES.CA_FIRM_ADMIN, USER_ROLES.CA_REVIEWER, USER_ROLES.ADMIN]}>
                    <ClientPortfolioPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/ca/review"
                element={
                  <ProtectedRoute allowedRoles={[USER_ROLES.CA_FIRM_ADMIN, USER_ROLES.CA_REVIEWER, USER_ROLES.ADMIN]}>
                    <DocumentReviewPage />
                  </ProtectedRoute>
                }
              />

              {/* ── Admin Routes ─────────────────────────────────────── */}
              <Route
                path="/admin/scrapers"
                element={
                  <ProtectedRoute allowedRoles={[USER_ROLES.ADMIN]}>
                    <ScraperHealthPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/runs"
                element={
                  <ProtectedRoute allowedRoles={[USER_ROLES.ADMIN]}>
                    <ScraperRunsPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/users"
                element={
                  <ProtectedRoute allowedRoles={[USER_ROLES.ADMIN]}>
                    <UserManagementPage />
                  </ProtectedRoute>
                }
              />
            </Route>

            {/* ── Error Routes ─────────────────────────────────────── */}
            <Route path="/unauthorized" element={<UnauthorizedPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;

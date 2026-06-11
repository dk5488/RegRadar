/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — App Root
   React Router setup with role-based route protection.
   ═══════════════════════════════════════════════════════════════════════ */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import ProtectedRoute from './components/common/ProtectedRoute';
import { USER_ROLES } from './utils/constants';

// ── Page imports (placeholders for now, replaced module-by-module) ────
import {
  LoginPage,
  RegisterPage,
  OnboardingPage,
  AlertInboxPage,
  AlertDetailPage,
  CalendarPage,
  ProfileSettingsPage,
  CADashboardPage,
  ClientPortfolioPage,
  DocumentReviewPage,
  ScraperHealthPage,
  ScraperRunsPage,
  UserManagementPage,
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

            {/* ── Smart Dashboard Redirect ──────────────────────────── */}
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <DashboardRedirect />
                </ProtectedRoute>
              }
            />

            {/* ── MSME Owner Routes ────────────────────────────────── */}
            <Route
              path="/onboarding"
              element={
                <ProtectedRoute>
                  <OnboardingPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/alerts"
              element={
                <ProtectedRoute>
                  <AlertInboxPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/alerts/:alertId"
              element={
                <ProtectedRoute>
                  <AlertDetailPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/calendar"
              element={
                <ProtectedRoute>
                  <CalendarPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfileSettingsPage />
                </ProtectedRoute>
              }
            />

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

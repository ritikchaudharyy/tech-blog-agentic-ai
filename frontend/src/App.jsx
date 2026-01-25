import { Routes, Route, Navigate, useLocation } from 'react-router-dom';

import Login from './pages/Login';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';

import UserHome from './pages/UserHome';
import ArticleView from './pages/ArticleView';

import AdminDashboard from './pages/AdminDashboard';
import AdminContent from './pages/AdminContent';

import ProtectedRoute from './components/ProtectedRoute';
import RouteTransition from './components/RouteTransition';

const App = () => {
  const location = useLocation();

  return (
    <Routes location={location} key={location.pathname}>

      {/* ---------- PUBLIC AUTH ROUTES ---------- */}
      <Route
        path="/login"
        element={
          <RouteTransition>
            <Login />
          </RouteTransition>
        }
      />

      <Route
        path="/forgot-password"
        element={
          <RouteTransition>
            <ForgotPassword />
          </RouteTransition>
        }
      />

      <Route
        path="/reset-password"
        element={
          <RouteTransition>
            <ResetPassword />
          </RouteTransition>
        }
      />

      {/* ---------- USER ROUTES ---------- */}
      <Route
        path="/app"
        element={
          <ProtectedRoute role="user">
            <RouteTransition>
              <UserHome />
            </RouteTransition>
          </ProtectedRoute>
        }
      />

      <Route
        path="/app/article/:id"
        element={
          <ProtectedRoute role="user">
            <RouteTransition>
              <ArticleView />
            </RouteTransition>
          </ProtectedRoute>
        }
      />

      {/* ---------- ADMIN ROUTES ---------- */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute role="admin">
            <RouteTransition>
              <AdminDashboard />
            </RouteTransition>
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/content"
        element={
          <ProtectedRoute role="admin">
            <RouteTransition>
              <AdminContent />
            </RouteTransition>
          </ProtectedRoute>
        }
      />

      {/* ---------- FALLBACK ---------- */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
};

export default App;

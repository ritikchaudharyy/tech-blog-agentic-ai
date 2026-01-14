import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Login from './pages/Login';
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
      <Route
        path="/login"
        element={
          <RouteTransition>
            <Login />
          </RouteTransition>
        }
      />

      {/* User */}
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

      {/* Admin */}
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

      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
};

export default App;

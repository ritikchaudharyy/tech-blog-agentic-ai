import { Navigate } from 'react-router-dom';
import { auth } from '../auth/auth';

const ProtectedRoute = ({ children, role }) => {
  if (!auth.isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (role && auth.role !== role) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;

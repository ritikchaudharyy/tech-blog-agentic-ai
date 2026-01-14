import { NavLink, useNavigate } from 'react-router-dom';
import ThemeToggle from '../components/ThemeToggle';

const AdminLayout = ({ children }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('API_KEY');
    localStorage.removeItem('USER_ROLE');
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex bg-muted dark:bg-slate-950">
      {/* Sidebar */}
      <aside className="sidebar w-64 min-h-screen px-4 py-6 bg-secondary dark:bg-slate-900 border-r border-light dark:border-white/10 flex flex-col">
        {/* Brand + Theme Toggle */}
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-lg font-semibold text-primary dark:text-white">
            Antigravity Admin
          </h2>
          <ThemeToggle />
        </div>

        {/* Navigation */}
        <nav className="flex flex-col gap-3 text-sm flex-1">
          <NavLink
            to="/admin"
            end
            className={({ isActive }) =>
              isActive
                ? 'font-semibold text-white bg-blue-600 px-3 py-2 rounded'
                : 'opacity-80 hover:opacity-100 px-3 py-2'
            }
          >
            Dashboard
          </NavLink>

          <NavLink
            to="/admin/content"
            className={({ isActive }) =>
              isActive
                ? 'font-semibold text-white bg-blue-600 px-3 py-2 rounded'
                : 'opacity-80 hover:opacity-100 px-3 py-2'
            }
          >
            Content
          </NavLink>
        </nav>

        {/* Logout */}
        <button
          onClick={handleLogout}
          className="mt-6 text-xs opacity-70 hover:opacity-100 text-left px-3 py-2 rounded hover:bg-red-500/10"
        >
          Logout
        </button>
      </aside>

      {/* Main */}
      <main className="flex-1 p-10 text-primary dark:text-slate-100">
        {children}
      </main>
    </div>
  );
};

export default AdminLayout;

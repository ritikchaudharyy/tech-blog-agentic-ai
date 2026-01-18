import { NavLink, useNavigate } from 'react-router-dom';
import { Home, Compass, BookOpen, Search, LogOut, Sparkles } from 'lucide-react';
import ThemeToggle from '../components/ThemeToggle';
import LanguageSelector from '../components/LanguageSelector';

const UserLayout = ({ children }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('API_KEY');
    localStorage.removeItem('USER_ROLE');
    localStorage.removeItem('auth_session');
    navigate('/login');
  };

  const navItems = [
    { to: '/app', label: 'Home', icon: Home, end: true },
    { to: '/app/explore', label: 'Explore', icon: Compass },
    { to: '/app/library', label: 'My Library', icon: BookOpen },
    { to: '/app/search', label: 'Search', icon: Search },
  ];

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/40 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
      {/* Sidebar */}
      <aside className="w-64 min-h-screen bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-r border-slate-200/50 dark:border-slate-800/50 flex flex-col shadow-sm">
        {/* Brand */}
        <div className="px-6 py-6 border-b border-slate-200/50 dark:border-slate-800/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900 dark:text-white tracking-tight">
                AI Content Platform
              </h2>
              <p className="text-[10px] text-slate-500 dark:text-slate-400 font-medium">
                Knowledge Hub
              </p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 group ${
                    isActive
                      ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/50'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <Icon className={`w-5 h-5 ${isActive ? '' : 'group-hover:scale-110 transition-transform'}`} />
                    <span className="font-medium text-sm">{item.label}</span>
                  </>
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* Theme, Language & Logout */}
        <div className="px-4 py-4 border-t border-slate-200/50 dark:border-slate-800/50 space-y-3">
          <div className="flex items-center gap-2 px-4">
            <ThemeToggle />
            <LanguageSelector />
          </div>
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-red-50 dark:hover:bg-red-950/20 hover:text-red-600 transition-all duration-200 group"
          >
            <LogOut className="w-5 h-5 group-hover:scale-110 transition-transform" />
            <span className="font-medium text-sm">Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
  );
};

export default UserLayout;
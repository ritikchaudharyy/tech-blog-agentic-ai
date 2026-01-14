import { Link, useNavigate } from 'react-router-dom';
import { LogOut } from 'lucide-react';
import ThemeToggle from './ThemeToggle';

const Navbar = ({ role }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('API_KEY');
    localStorage.removeItem('USER_ROLE');
    navigate('/');
  };

  return (
    <header className="sticky top-0 z-40 w-full backdrop-blur-xl bg-white/70 dark:bg-slate-950/70 border-b border-black/5 dark:border-white/10">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link
          to={role === 'admin' ? '/admin' : '/app'}
          className="text-lg font-bold tracking-tight text-slate-900 dark:text-slate-100"
        >
          Tech<span className="text-blue-600">Blog</span>
        </Link>

        {/* Right actions */}
        <div className="flex items-center gap-4">
          <ThemeToggle />

          <button
            onClick={handleLogout}
            className="flex items-center gap-1 text-sm text-slate-600 dark:text-slate-300 hover:text-red-600 transition"
          >
            <LogOut size={16} />
            Logout
          </button>
        </div>
      </div>
    </header>
  );
};

export default Navbar;

import LanguageSelector from '../components/LanguageSelector';
import ThemeToggle from '../components/ThemeToggle';

const UserLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-primary dark:bg-slate-950 text-primary dark:text-slate-100">
      {/* Header */}
      <header className="bg-secondary dark:bg-slate-900 border-b border-light dark:border-white/10">
        <div className="container flex justify-between items-center h-16">
          <h2 className="text-lg font-semibold">
            Antigravity
          </h2>

          <div className="flex items-center gap-6">
            <LanguageSelector />
            <ThemeToggle />
            <div className="text-sm text-secondary dark:text-slate-300">
              User
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container py-10">
        {children}
      </main>
    </div>
  );
};

export default UserLayout;

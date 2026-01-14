import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mail, Key, Lock, ShieldCheck } from 'lucide-react';
import { apiClient } from '../api/client';
import ThemeToggle from '../components/ThemeToggle';

const Login = () => {
  const [email, setEmail] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [error, setError] = useState(null);

  const navigate = useNavigate();
  const isAdmin = email === 'admin@example.com';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!email.trim()) return;

    if (isAdmin && !apiKey.trim()) {
      setError('Admin login requires an Owner API Key');
      return;
    }

    try {
      setIsLoggingIn(true);
      const res = await apiClient.post('/api/auth/login', {
        email,
        api_key: isAdmin ? apiKey : null,
      });

      if (res.api_key) localStorage.setItem('API_KEY', res.api_key);
      localStorage.setItem('USER_ROLE', res.role || 'user');

      navigate(res.role === 'admin' ? '/admin' : '/app');
    } catch (err) {
      setError(err.message || 'Authentication failed');
    } finally {
      setIsLoggingIn(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden">
      {/* Theme toggle */}
      <div className="absolute top-6 right-6 z-20">
        <ThemeToggle />
      </div>

      {/* Card */}
      <div className="relative w-full max-w-md px-4">
        <div className="glass p-8 animate-fade-in">
          <h1 className="mb-2">Welcome Back</h1>
          <p className="text-sm mb-8">Sign in to continue to your workspace</p>

          {error && (
            <div className="mb-4 text-sm text-red-500 bg-red-500/10 border border-red-500/20 p-3 rounded-lg">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="grid gap-5">
            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase opacity-70">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 opacity-60 w-4 h-4" />
                <input
                  type="email"
                  required
                  placeholder="name@company.com"
                  className="input pl-10"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>

            {isAdmin && (
              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase opacity-70">
                  Owner API Key
                </label>
                <div className="relative">
                  <Key className="absolute left-3 top-1/2 -translate-y-1/2 opacity-60 w-4 h-4" />
                  <input
                    type="password"
                    required
                    placeholder="sk_..."
                    className="input pl-10"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                  />
                  <Lock className="absolute right-3 top-1/2 -translate-y-1/2 opacity-50 w-3 h-3" />
                </div>
                <p className="text-[11px] opacity-60 flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3" />
                  Required for admin verification
                </p>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoggingIn}
              className="btn btn-primary w-full py-3 mt-2"
            >
              {isLoggingIn ? 'Verifying Identity…' : 'Secure Sign In'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;

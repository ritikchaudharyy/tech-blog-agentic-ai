import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mail, Key, Lock, ShieldCheck, Sparkles, ArrowLeft } from 'lucide-react';
import { auth } from '../auth/auth';
import ThemeToggle from '../components/ThemeToggle';

const ADMIN_EMAIL = 'arvik3cr@gmail.com';

const Login = () => {
  const [email, setEmail] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [error, setError] = useState(null);
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [resetEmail, setResetEmail] = useState('');
  const [resetSuccess, setResetSuccess] = useState(false);

  const navigate = useNavigate();
  const isAdmin = email === ADMIN_EMAIL;

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

      const payload = { email };
      if (isAdmin) {
        payload.api_key = apiKey;
      }

      const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(isAdmin && apiKey ? { 'X-API-Key': apiKey } : {}),
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Authentication failed');
      }

      const data = await res.json();

      auth.login(email, data.api_key);

      if (data.api_key) localStorage.setItem('API_KEY', data.api_key);
      localStorage.setItem('USER_ROLE', data.role || 'user');

      navigate(data.role === 'admin' ? '/admin' : '/app');
    } catch (err) {
      setError(err.message || 'Authentication failed');
    } finally {
      setIsLoggingIn(false);
    }
  };

  const handleForgotPassword = async (e) => {
    e.preventDefault();
    setError(null);

    if (!resetEmail.trim()) {
      setError('Please enter your email address');
      return;
    }

    try {
      setIsLoggingIn(true);

      const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/auth/forgot-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: resetEmail }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Failed to send reset email');
      }

      setResetSuccess(true);
      setTimeout(() => {
        setShowForgotPassword(false);
        setResetSuccess(false);
        setResetEmail('');
      }, 3000);
    } catch (err) {
      setError(err.message || 'Failed to send reset email');
    } finally {
      setIsLoggingIn(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden p-4 sm:p-6 lg:p-8">
      {/* Animated Background Blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 -left-4 w-56 h-56 sm:w-72 sm:h-72 bg-blue-500/20 dark:bg-blue-500/30 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-3xl animate-blob"></div>
        <div className="absolute top-0 -right-4 w-56 h-56 sm:w-72 sm:h-72 bg-purple-500/20 dark:bg-purple-500/30 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-3xl animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-12 sm:left-20 w-56 h-56 sm:w-72 sm:h-72 bg-indigo-500/20 dark:bg-indigo-500/30 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-3xl animate-blob animation-delay-4000"></div>
      </div>

      {/* Theme Toggle */}
      <div className="absolute top-4 right-4 sm:top-6 sm:right-6 z-20">
        <ThemeToggle />
      </div>

      {/* Login Card */}
      <div className="relative w-full max-w-md">
        <div className="glass-card animate-scale-in">
          {!showForgotPassword ? (
            <>
              {/* Header */}
              <div className="text-center mb-6 sm:mb-8">
                <div className="flex items-center justify-center gap-3 mb-4">
                  <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
                    <Sparkles className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
                  </div>
                </div>
                <h1 className="text-2xl sm:text-3xl font-bold mb-2 text-gradient">Welcome Back</h1>
                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 px-2">
                  Sign in to continue to your workspace
                </p>
              </div>

              {/* Error Message */}
              {error && (
                <div className="mb-5 sm:mb-6 p-3 sm:p-4 rounded-xl bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/50 animate-slide-in">
                  <p className="text-xs sm:text-sm text-red-600 dark:text-red-400">{error}</p>
                </div>
              )}

              {/* Form */}
              <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-5">
                {/* Email Input */}
                <div className="space-y-2">
                  <label className="text-xs font-semibold uppercase text-slate-600 dark:text-slate-400 tracking-wider">
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 sm:left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
                    <input
                      type="email"
                      required
                      placeholder="name@company.com"
                      className="input pl-10 sm:pl-11 text-sm sm:text-base"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </div>
                </div>

                {/* Admin API Key Input */}
                {isAdmin && (
                  <div className="space-y-2 animate-slide-in">
                    <label className="text-xs font-semibold uppercase text-slate-600 dark:text-slate-400 tracking-wider">
                      Owner API Key
                    </label>
                    <div className="relative">
                      <Key className="absolute left-3 sm:left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
                      <input
                        type="password"
                        required
                        placeholder="Enter your owner API key"
                        className="input pl-10 sm:pl-11 pr-10 sm:pr-11 text-sm sm:text-base"
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                      />
                      <Lock className="absolute right-3 sm:right-4 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none" />
                    </div>
                    <div className="flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-500">
                      <ShieldCheck className="w-3.5 h-3.5 flex-shrink-0" />
                      <span>Required for admin verification</span>
                    </div>
                  </div>
                )}

                {/* Forgot Password Link */}
                <div className="flex items-center justify-end">
                  <button
                    type="button"
                    onClick={() => setShowForgotPassword(true)}
                    className="text-xs sm:text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors"
                  >
                    Forgot password?
                  </button>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={isLoggingIn}
                  className="btn btn-primary w-full py-2.5 sm:py-3 mt-4 sm:mt-6 text-sm sm:text-base"
                >
                  {isLoggingIn ? (
                    <div className="flex items-center gap-2">
                      <div className="spinner"></div>
                      <span>Verifying Identity...</span>
                    </div>
                  ) : (
                    'Secure Sign In'
                  )}
                </button>
              </form>
            </>
          ) : (
            <>
              {/* Forgot Password Form */}
              <div className="animate-fade-in">
                {/* Header */}
                <div className="mb-6 sm:mb-8">
                  <button
                    onClick={() => {
                      setShowForgotPassword(false);
                      setError(null);
                      setResetEmail('');
                    }}
                    className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition-colors mb-4 sm:mb-6"
                  >
                    <ArrowLeft className="w-4 h-4" />
                    Back to login
                  </button>
                  <h2 className="text-2xl sm:text-3xl font-bold mb-2 text-gradient">Reset Password</h2>
                  <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 px-2">
                    Enter your email and we'll send you a reset link
                  </p>
                </div>

                {/* Success Message */}
                {resetSuccess && (
                  <div className="mb-5 sm:mb-6 p-3 sm:p-4 rounded-xl bg-green-50 dark:bg-green-950/20 border border-green-200 dark:border-green-900/50 animate-slide-in">
                    <p className="text-xs sm:text-sm text-green-600 dark:text-green-400">
                      Reset link sent! Check your email.
                    </p>
                  </div>
                )}

                {/* Error Message */}
                {error && (
                  <div className="mb-5 sm:mb-6 p-3 sm:p-4 rounded-xl bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/50 animate-slide-in">
                    <p className="text-xs sm:text-sm text-red-600 dark:text-red-400">{error}</p>
                  </div>
                )}

                {/* Reset Form */}
                <form onSubmit={handleForgotPassword} className="space-y-4 sm:space-y-5">
                  <div className="space-y-2">
                    <label className="text-xs font-semibold uppercase text-slate-600 dark:text-slate-400 tracking-wider">
                      Email Address
                    </label>
                    <div className="relative">
                      <Mail className="absolute left-3 sm:left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
                      <input
                        type="email"
                        required
                        placeholder="name@company.com"
                        className="input pl-10 sm:pl-11 text-sm sm:text-base"
                        value={resetEmail}
                        onChange={(e) => setResetEmail(e.target.value)}
                      />
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={isLoggingIn || resetSuccess}
                    className="btn btn-primary w-full py-2.5 sm:py-3 mt-4 sm:mt-6 text-sm sm:text-base"
                  >
                    {isLoggingIn ? (
                      <div className="flex items-center gap-2">
                        <div className="spinner"></div>
                        <span>Sending...</span>
                      </div>
                    ) : resetSuccess ? (
                      'Email Sent ✓'
                    ) : (
                      'Send Reset Link'
                    )}
                  </button>
                </form>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Login;
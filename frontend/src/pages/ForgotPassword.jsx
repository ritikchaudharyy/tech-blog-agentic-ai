import { useState } from 'react';
import { Mail } from 'lucide-react';
import AnimatedBackground from '../components/AnimatedBackground';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      setLoading(true);
      const res = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/auth/forgot-password`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email }),
        }
      );

      if (!res.ok) throw new Error('Unable to send reset link');
      setSent(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center px-4">
      <AnimatedBackground />

      <div className="glass w-full max-w-sm p-8 rounded-2xl animate-slide-in">
        <h1 className="text-2xl font-semibold text-center mb-2">
          Reset Password
        </h1>
        <p className="text-sm text-center opacity-70 mb-6">
          We’ll send you a secure reset link
        </p>

        {sent ? (
          <p className="text-center text-green-600 text-sm">
            Reset link sent. Check your email.
          </p>
        ) : (
          <form onSubmit={handleSubmit} className="grid gap-5">
            {error && (
              <div className="text-sm text-red-500 bg-red-500/10 p-3 rounded-lg">
                {error}
              </div>
            )}

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

            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary w-full py-3"
            >
              {loading ? 'Sending…' : 'Send Reset Link'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default ForgotPassword;

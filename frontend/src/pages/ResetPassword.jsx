import { useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import AnimatedBackground from '../components/AnimatedBackground';

const ResetPassword = () => {
  const [params] = useSearchParams();
  const token = params.get('token');
  const navigate = useNavigate();

  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      setLoading(true);
      const res = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/auth/reset-password`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token, password }),
        }
      );

      if (!res.ok) throw new Error('Invalid or expired token');
      navigate('/');
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
        <h1 className="text-2xl font-semibold text-center mb-6">
          Set New Password
        </h1>

        {error && (
          <div className="text-sm text-red-500 bg-red-500/10 p-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="grid gap-5">
          <input
            type="password"
            required
            placeholder="New password"
            className="input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary w-full py-3"
          >
            {loading ? 'Updating…' : 'Update Password'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ResetPassword;

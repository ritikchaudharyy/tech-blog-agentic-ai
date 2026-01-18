import { useState, useEffect, useCallback } from 'react';
import { TrendingUp, Clock, Eye, Sparkles, Search, Bell, User, ChevronDown } from 'lucide-react';
import { Link } from 'react-router-dom';
import UserLayout from '../layouts/UserLayout';
import { userAPI } from '../api/user.api';

const UserHome = () => {
  const [loading, setLoading] = useState(true);
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState(null);

  const fetchTrendingArticles = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await userAPI.getTrending();
      setArticles(Array.isArray(res) ? res : []);
    } catch (err) {
      setError(err.message || 'Failed to load trending articles');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTrendingArticles();
  }, [fetchTrendingArticles]);

  return (
    <UserLayout>
      <div className="max-w-7xl mx-auto px-8 py-8 space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                type="text"
                placeholder="Search articles..."
                className="w-80 h-11 pl-11 pr-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
              />
            </div>
          </div>

          <div className="flex items-center gap-4">
            <button className="relative p-2.5 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
              <Bell className="w-5 h-5 text-slate-600 dark:text-slate-400" />
            </button>
            <div className="flex items-center gap-3 pl-4 border-l border-slate-200 dark:border-slate-700">
              <div className="w-9 h-9 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center text-white shadow-lg">
                <User className="w-5 h-5" />
              </div>
              <ChevronDown className="w-4 h-4 text-slate-400" />
            </div>
          </div>
        </div>

        {/* Welcome Banner */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-8 text-white shadow-xl shadow-blue-500/20">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles className="w-5 h-5" />
            <span className="text-sm font-semibold">Welcome to Knowledge Hub</span>
          </div>
          <h1 className="text-3xl font-bold mb-2">
            Explore AI-Powered Articles & Insights
          </h1>
          <p className="text-blue-100 text-base">
            Discover trending content, expand your knowledge, and stay ahead in technology.
          </p>
        </div>

        {/* Trending Section */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <TrendingUp className="w-6 h-6 text-orange-500" />
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Trending Articles
              </h2>
            </div>
            <button
              onClick={fetchTrendingArticles}
              className="text-sm font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 transition-colors"
            >
              Refresh
            </button>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 animate-pulse"
                >
                  <div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-3/4 mb-4"></div>
                  <div className="h-3 bg-slate-200 dark:bg-slate-800 rounded w-full mb-2"></div>
                  <div className="h-3 bg-slate-200 dark:bg-slate-800 rounded w-2/3"></div>
                </div>
              ))}
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/50 rounded-2xl p-6 text-red-600 dark:text-red-400">
              {error}
            </div>
          )}

          {/* Articles Grid */}
          {!loading && !error && articles.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {articles.map((article) => (
                <Link
                  key={article.id}
                  to={`/app/article/${article.id}`}
                  className="group bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 hover:shadow-xl hover:shadow-slate-200/50 dark:hover:shadow-slate-900/50 transition-all duration-300 overflow-hidden"
                >
                  <div className="p-6 space-y-4">
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors line-clamp-2">
                      {article.title}
                    </h3>
                    <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-3">
                      {article.meta_description || 'Discover insights and knowledge in this comprehensive article.'}
                    </p>
                    <div className="flex items-center justify-between pt-2 text-xs text-slate-500 dark:text-slate-500">
                      <div className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5" />
                        <span>5 min read</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Eye className="w-3.5 h-3.5" />
                        <span>{(article.view_count || 0).toLocaleString()} views</span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}

          {/* Empty State */}
          {!loading && !error && articles.length === 0 && (
            <div className="flex flex-col items-center justify-center py-20 bg-white dark:bg-slate-900 rounded-2xl border border-dashed border-slate-200 dark:border-slate-800">
              <div className="bg-blue-50 dark:bg-blue-950/20 p-6 rounded-full mb-6">
                <TrendingUp className="w-12 h-12 text-blue-500" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
                No trending articles yet
              </h3>
              <p className="text-slate-500 dark:text-slate-400 mb-6 text-center max-w-md">
                Articles will appear here once content starts gaining traction. Check back soon!
              </p>
              <button
                onClick={fetchTrendingArticles}
                className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold shadow-lg shadow-blue-500/30 hover:shadow-xl hover:shadow-blue-500/40 transition-all"
              >
                Refresh
              </button>
            </div>
          )}
        </div>
      </div>
    </UserLayout>
  );
};

export default UserHome;
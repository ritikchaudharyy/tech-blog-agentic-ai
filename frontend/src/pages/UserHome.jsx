import { useState, useEffect } from 'react';
import { Compass } from 'lucide-react';
import { Link } from 'react-router-dom';
import UserLayout from '../layouts/UserLayout';
import Skeleton from '../components/Skeleton';
import { apiClient } from '../api/client';

const UserHome = () => {
  const [loading, setLoading] = useState(true);
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTrendingArticles = async () => {
      try {
        setLoading(true);
        const res = await apiClient.get('/api/articles/trending');
        setArticles(res || []);
      } catch (err) {
        setError(err.message || 'Failed to load trending articles');
      } finally {
        setLoading(false);
      }
    };

    fetchTrendingArticles();
  }, []);

  return (
    <UserLayout>
      <div className="space-y-10 animate-fade-in">
        {/* Header */}
        <div className="flex justify-between items-end border-b border-gray-100 pb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 tracking-tight mb-2">
              Tech Blog Dashboard
            </h1>
            <p className="text-secondary text-sm">
              Explore the latest in Artificial Intelligence
            </p>
          </div>
        </div>

        {/* Error State */}
        {error && (
          <div className="text-red-600 bg-red-50 border border-red-100 p-4 rounded-lg">
            {error}
          </div>
        )}

        {/* Loading State */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[1, 2, 3].map((i) => (
              <div key={i} className="space-y-4">
                <Skeleton height="180px" className="w-full rounded-xl" />
                <div className="space-y-2">
                  <Skeleton variant="text" className="w-3/4 h-6" />
                  <Skeleton variant="text" className="w-1/2 h-4" />
                </div>
                <div className="flex gap-2 pt-2">
                  <Skeleton variant="circle" className="w-8 h-8" />
                  <Skeleton variant="text" className="w-24 h-4 mt-2" />
                </div>
              </div>
            ))}
          </div>
        ) : articles.length > 0 ? (
          /* Trending Articles */
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {articles.map((article) => (
              <Link
                key={article.id}
                to={`/articles/${article.id}`}
                className="group bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow overflow-hidden"
              >
                <div className="p-6 space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                    {article.title}
                  </h3>
                  <p className="text-sm text-gray-500 line-clamp-3">
                    {article.excerpt}
                  </p>
                  <div className="flex items-center justify-between pt-2 text-xs text-gray-400">
                    <span>{article.author}</span>
                    <span>{article.views?.toLocaleString() || 0} views</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          /* Empty State */
          <div className="flex flex-col items-center justify-center py-20 bg-white rounded-2xl border border-dashed border-gray-200 text-center">
            <div className="bg-blue-50 p-6 rounded-full mb-6 animate-bounce-slow">
              <Compass size={48} className="text-blue-500" />
            </div>

            <h2 className="text-2xl font-bold text-gray-900 mb-3">
              No trending articles yet
            </h2>
            <p className="text-gray-500 max-w-md mb-8 leading-relaxed">
              Articles will appear here once content starts gaining traction.
              Check back soon or explore other sections.
            </p>

            <div className="flex gap-4">
              <button
                onClick={() => window.location.reload()}
                className="btn btn-primary px-6 py-2.5 shadow-lg shadow-blue-200"
              >
                Refresh
              </button>
              <Link
                to="/search"
                className="px-6 py-2.5 rounded-lg font-medium text-gray-600 hover:bg-gray-50 transition-colors"
              >
                Search Articles
              </Link>
            </div>
          </div>
        )}
      </div>
    </UserLayout>
  );
};

export default UserHome;

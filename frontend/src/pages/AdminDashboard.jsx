import { useState, useEffect } from 'react';
import { LineChart, Line, ResponsiveContainer, Tooltip } from 'recharts';
import { MoreHorizontal, FileText, Users, DollarSign, ArrowUpRight } from 'lucide-react';
import AdminLayout from '../layouts/AdminLayout';
import { apiClient } from '../api/client';

const AdminDashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [traffic, setTraffic] = useState([]);
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [metricsRes, trafficRes, articlesRes] = await Promise.all([
          apiClient.get('/api/admin/metrics'),
          apiClient.get('/api/admin/traffic'),
          apiClient.get('/api/admin/articles'),
        ]);

        setMetrics(metricsRes);
        setTraffic(trafficRes || []);
        setArticles(articlesRes || []);
      } catch (err) {
        setError(err.message || 'Failed to load admin dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <AdminLayout>
        <div className="p-6 text-gray-500">Loading dashboard data…</div>
      </AdminLayout>
    );
  }

  if (error) {
    return (
      <AdminLayout>
        <div className="p-6 text-red-600">Error: {error}</div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="animate-fade-in space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Admin Overview</h1>
            <p className="text-sm text-gray-500 mt-1">
              Monitor your platform&apos;s growth and performance
            </p>
          </div>
          <div className="flex items-center gap-3 bg-white px-4 py-2 rounded-full border border-gray-200 shadow-sm">
            <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-xs">
              EA
            </div>
            <div>
              <p className="text-xs font-bold text-gray-700 leading-none">
                Enterprise Admin
              </p>
              <p className="text-[10px] text-green-600 font-medium leading-none mt-1">
                ● Verified Active
              </p>
            </div>
          </div>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <StatCard
            title="Total Views"
            value={metrics.totalViews?.toLocaleString() || '0'}
            trend={metrics.viewsGrowth || '+0%'}
            icon={<FileText size={18} className="text-white" />}
            iconBg="bg-blue-500"
            data={traffic.views || []}
            color="#3b82f6"
          />
          <StatCard
            title="Active Users"
            value={metrics.activeUsers?.toLocaleString() || '0'}
            trend={metrics.usersGrowth || '+0%'}
            icon={<Users size={18} className="text-white" />}
            iconBg="bg-green-500"
            data={traffic.users || []}
            color="#22c55e"
          />
          <StatCard
            title="Total Revenue"
            value={`$${metrics.revenue?.toLocaleString() || '0'}`}
            trend={metrics.revenueGrowth || '+0%'}
            icon={<DollarSign size={18} className="text-white" />}
            iconBg="bg-purple-500"
            data={traffic.revenue || []}
            color="#a855f7"
          />
        </div>

        {/* Recent Articles */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="px-6 py-5 border-b border-gray-100 flex justify-between items-center bg-gray-50/30">
            <div>
              <h3 className="font-semibold text-gray-900">Recent Articles</h3>
              <p className="text-xs text-gray-500 mt-0.5">
                Manage your latest content submissions
              </p>
            </div>
            <button className="text-gray-400 hover:text-gray-600 p-1 hover:bg-gray-100 rounded">
              <MoreHorizontal size={20} />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-gray-50 border-b border-gray-100 text-gray-500 font-medium text-xs uppercase tracking-wider">
                <tr>
                  <th className="px-6 py-4">Article Title</th>
                  <th className="px-6 py-4">Author</th>
                  <th className="px-6 py-4">Publish Date</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {articles.length === 0 && (
                  <tr>
                    <td colSpan="5" className="px-6 py-6 text-center text-gray-400">
                      No articles found
                    </td>
                  </tr>
                )}
                {articles.map((article) => (
                  <ArticleRow
                    key={article.id}
                    title={article.title}
                    author={article.author}
                    date={article.published_at}
                    status={article.status}
                  />
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

/* ---------------- Sub Components ---------------- */

const StatCard = ({ title, value, trend, icon, iconBg, data, color }) => (
  <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col justify-between h-56">
    <div className="flex justify-between items-start mb-2">
      <div>
        <div className="flex items-center gap-2 mb-2">
          <div className={`p-1.5 rounded-lg ${iconBg}`}>{icon}</div>
          <span className="text-sm font-medium text-gray-500">{title}</span>
        </div>
        <h3 className="text-3xl font-bold text-gray-900">{value}</h3>
      </div>
      <div className="flex items-center text-green-600 text-xs font-bold bg-green-50 px-2 py-1 rounded-full">
        {trend}
        <ArrowUpRight size={12} className="ml-0.5" />
      </div>
    </div>

    <div className="h-20 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <Line
            type="monotone"
            dataKey="val"
            stroke={color}
            strokeWidth={3}
            dot={false}
          />
          <Tooltip cursor={false} content={<></>} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  </div>
);

const ArticleRow = ({ title, author, date, status }) => (
  <tr className="hover:bg-gray-50 transition-colors group">
    <td className="px-6 py-4 font-medium text-gray-900">{title}</td>
    <td className="px-6 py-4 text-gray-600">{author}</td>
    <td className="px-6 py-4 text-gray-500">{date}</td>
    <td className="px-6 py-4">
      <span
        className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold ${
          status === 'Published'
            ? 'bg-green-100 text-green-700'
            : 'bg-gray-100 text-gray-600'
        }`}
      >
        {status}
      </span>
    </td>
    <td className="px-6 py-4 text-right">
      <button className="text-gray-300 hover:text-gray-700 p-1.5 hover:bg-gray-200 rounded-md">
        <MoreHorizontal size={16} />
      </button>
    </td>
  </tr>
);

export default AdminDashboard;

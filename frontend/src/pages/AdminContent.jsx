import { useState, useEffect } from 'react';
import { Edit, MoreHorizontal, FileText, CheckCircle, Clock, Trash2 } from 'lucide-react';
import AdminLayout from '../layouts/AdminLayout';
import { apiClient } from '../api/client';

const AdminContent = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchArticles = async () => {
    try {
      setLoading(true);
      const res = await apiClient.get('/api/admin/articles');
      setArticles(res || []);
    } catch (err) {
      setError(err.message || 'Failed to load articles');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArticles();
  }, []);

  const handlePublish = async (id) => {
    try {
      await apiClient.post(`/api/admin/articles/${id}/publish`);
      fetchArticles();
    } catch (err) {
      alert(err.message || 'Failed to publish article');
    }
  };

  const handleDelete = async (id) => {
    const confirmDelete = window.confirm('Are you sure you want to delete this article?');
    if (!confirmDelete) return;

    try {
      await apiClient.post(`/api/admin/articles/${id}/delete`);
      fetchArticles();
    } catch (err) {
      alert(err.message || 'Failed to delete article');
    }
  };

  return (
    <AdminLayout>
      <div className="animate-fade-in space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 tracking-tight">
              Content Management
            </h1>
            <p className="text-sm text-gray-500 mt-1">
              Create, edit, and moderate platform content
            </p>
          </div>
          <button className="btn btn-primary px-4 py-2 flex items-center gap-2 shadow-sm">
            <FileText size={16} />
            <span>New Article</span>
          </button>
        </div>

        {/* State handling */}
        {loading && (
          <div className="text-gray-500 text-sm">Loading articles…</div>
        )}

        {error && (
          <div className="text-red-600 text-sm">Error: {error}</div>
        )}

        {!loading && !error && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-gray-50 border-b border-gray-100 text-gray-500 font-medium text-xs uppercase tracking-wider">
                  <tr>
                    <th className="px-6 py-4">Article Title</th>
                    <th className="px-6 py-4">Status</th>
                    <th className="px-6 py-4">Verification</th>
                    <th className="px-6 py-4">Views</th>
                    <th className="px-6 py-4 text-right">Actions</th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-gray-50">
                  {articles.length === 0 && (
                    <tr>
                      <td
                        colSpan="5"
                        className="px-6 py-6 text-center text-gray-400"
                      >
                        No articles found
                      </td>
                    </tr>
                  )}

                  {articles.map((article) => (
                    <tr
                      key={article.id}
                      className="hover:bg-gray-50/60 transition-colors group"
                    >
                      <td className="px-6 py-4 font-medium text-gray-900">
                        {article.title}
                      </td>

                      <td className="px-6 py-4">
                        <span
                          className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold ${
                            article.status === 'Published'
                              ? 'bg-green-100 text-green-700 border border-green-200'
                              : 'bg-gray-100 text-gray-600 border border-gray-200'
                          }`}
                        >
                          <span
                            className={`w-1.5 h-1.5 rounded-full mr-1.5 ${
                              article.status === 'Published'
                                ? 'bg-green-500'
                                : 'bg-gray-400'
                            }`}
                          ></span>
                          {article.status}
                        </span>
                      </td>

                      <td className="px-6 py-4">
                        {article.verified ? (
                          <div className="flex items-center gap-1.5 text-green-700 text-xs font-medium bg-green-50 w-fit px-2 py-1 rounded border border-green-100">
                            <CheckCircle size={12} /> Verified
                          </div>
                        ) : (
                          <div className="flex items-center gap-1.5 text-amber-700 text-xs font-medium bg-amber-50 w-fit px-2 py-1 rounded border border-amber-100">
                            <Clock size={12} /> Pending
                          </div>
                        )}
                      </td>

                      <td className="px-6 py-4 text-gray-500 font-mono text-xs">
                        {(article.views || 0).toLocaleString()}
                      </td>

                      <td className="px-6 py-4 text-right">
                        <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                          {article.status !== 'Published' && (
                            <button
                              onClick={() => handlePublish(article.id)}
                              className="p-1.5 hover:bg-gray-100 rounded text-green-600 transition-colors"
                              title="Publish"
                            >
                              <CheckCircle size={16} />
                            </button>
                          )}
                          <button
                            className="p-1.5 hover:bg-gray-100 rounded text-gray-500 hover:text-blue-600 transition-colors"
                            title="Edit"
                          >
                            <Edit size={16} />
                          </button>
                          <button
                            onClick={() => handleDelete(article.id)}
                            className="p-1.5 hover:bg-gray-100 rounded text-red-500 transition-colors"
                            title="Delete"
                          >
                            <Trash2 size={16} />
                          </button>
                          <button className="p-1.5 hover:bg-gray-100 rounded text-gray-500 transition-colors">
                            <MoreHorizontal size={16} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </AdminLayout>
  );
};

export default AdminContent;

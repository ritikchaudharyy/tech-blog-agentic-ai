import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle, Clock } from 'lucide-react';
import UserLayout from '../layouts/UserLayout';
import Skeleton from '../components/Skeleton';
import { apiClient } from '../api/client';

const ArticleView = () => {
  const { id } = useParams();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        setLoading(true);
        const res = await apiClient.get(`/api/articles/${id}`);
        setArticle(res);
      } catch (err) {
        setError(err.message || 'Failed to load article');
      } finally {
        setLoading(false);
      }
    };

    fetchArticle();
  }, [id]);

  if (loading) {
    return (
      <UserLayout>
        <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
          <Skeleton className="w-24 h-6" />
          <div className="space-y-4">
            <Skeleton className="w-3/4 h-12 rounded-lg" />
            <Skeleton className="w-1/2 h-6" />
          </div>
          <Skeleton className="w-full h-64 rounded-xl" />
        </div>
      </UserLayout>
    );
  }

  if (error) {
    return (
      <UserLayout>
        <div className="max-w-4xl mx-auto py-12 text-red-600">
          Error: {error}
        </div>
      </UserLayout>
    );
  }

  if (!article) {
    return (
      <UserLayout>
        <div className="max-w-4xl mx-auto py-12 text-gray-500">
          Article not found
        </div>
      </UserLayout>
    );
  }

  return (
    <UserLayout>
      <div className="max-w-4xl mx-auto animate-fade-in">
        <Link
          to="/app"
          className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-blue-600 mb-8 transition-colors"
        >
          <ArrowLeft size={16} /> Back to Dashboard
        </Link>

        <header className="mb-10 pb-10 border-b border-gray-100">
          <div className="flex items-center gap-3 mb-4">
            {article.verified && (
              <span className="inline-flex items-center gap-1.5 text-xs font-medium text-green-700 bg-green-50 px-3 py-1 rounded-full border border-green-100">
                <CheckCircle size={12} className="fill-green-600 text-white" />
                Verified Source
              </span>
            )}
            <span className="text-xs text-gray-500 flex items-center gap-1">
              <Clock size={12} />
              {article.read_time || '5 min read'}
            </span>
          </div>

          <h1 className="text-4xl font-bold text-gray-900 leading-tight mb-6">
            {article.title}
          </h1>

          {article.summary && (
            <p className="text-xl text-gray-500 leading-relaxed font-light">
              {article.summary}
            </p>
          )}

          <div className="flex items-center gap-3 mt-8">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-100 to-indigo-100"></div>
            <div>
              <p className="text-sm font-semibold text-gray-900">
                {article.author}
              </p>
              <p className="text-xs text-gray-500">
                {article.date}
              </p>
            </div>
          </div>
        </header>

        <article className="prose prose-blue max-w-none text-gray-600 space-y-12">
          {article.content?.sections?.map((section, index) => (
            <section key={index}>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                {section.heading}
              </h3>

              {section.text && (
                <p className="leading-7 mb-4">
                  {section.text}
                </p>
              )}

              {section.bullets && (
                <ul className="list-disc pl-6 space-y-2 marker:text-blue-500">
                  {section.bullets.map((item, i) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              )}
            </section>
          ))}
        </article>
      </div>
    </UserLayout>
  );
};

export default ArticleView;

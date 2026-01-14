import React, { useEffect, useState } from 'react';
import { getDashboardOverview, getWeakCTRArticles } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertTriangle, CheckCircle, TrendingUp, FileText } from 'lucide-react';

const Dashboard = () => {
    const [stats, setStats] = useState(null);
    const [weakArticles, setWeakArticles] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchData() {
            try {
                const [overviewData, weakData] = await Promise.all([
                    getDashboardOverview(),
                    getWeakCTRArticles()
                ]);
                setStats(overviewData);
                setWeakArticles(weakData);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    if (loading) return <div className="p-10 text-center">Loading Dashboard...</div>;
    if (!stats) return <div className="p-10 text-center text-red-500">Failed to load data. Check Backend.</div>;

    return (
        <div className="p-6 max-w-7xl mx-auto bg-slate-50 min-h-screen">
            <h1 className="text-3xl font-bold mb-8 text-slate-800">Agentic Knowledge Dashboard</h1>

            {/* KPI CARDS */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
                <KpiCard
                    title="Total Articles"
                    value={stats.total_articles}
                    icon={<FileText className="w-8 h-8 text-blue-500" />}
                />
                <KpiCard
                    title="Published"
                    value={stats.published_articles}
                    icon={<CheckCircle className="w-8 h-8 text-green-500" />}
                />
                <KpiCard
                    title="Drafts"
                    value={stats.draft_articles}
                    icon={<FileText className="w-8 h-8 text-gray-400" />}
                />
                <KpiCard
                    title="Weak CTR"
                    value={stats.weak_ctr_articles}
                    icon={<AlertTriangle className="w-8 h-8 text-orange-500" />}
                    alert={stats.weak_ctr_articles > 0}
                />
            </div>

            {/* MAIN CONTENT AREA */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                {/* LOW PERFORMING ARTICLES */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                    <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                        <TrendingUp className="w-5 h-5 text-indigo-600" />
                        CTR Attention Needed
                    </h2>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-slate-50 text-slate-600 uppercase text-xs">
                                <tr>
                                    <th className="px-4 py-3">Title</th>
                                    <th className="px-4 py-3">Views</th>
                                    <th className="px-4 py-3">Status</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {weakArticles.map((article) => (
                                    <tr key={article.id} className="hover:bg-slate-50">
                                        <td className="px-4 py-3 font-medium text-slate-700 truncate max-w-xs">{article.title}</td>
                                        <td className="px-4 py-3 text-slate-500">{article.views}</td>
                                        <td className="px-4 py-3">
                                            <StatusBadge status={article.ctr_status} />
                                        </td>
                                    </tr>
                                ))}
                                {weakArticles.length === 0 && (
                                    <tr>
                                        <td colSpan="3" className="px-4 py-8 text-center text-slate-400">
                                            All articles are performing well!
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* PLACEHOLDER CHART (Since we don't have history yet) */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex flex-col justify-center items-center text-center">
                    <div className="bg-blue-50 p-4 rounded-full mb-4">
                        <TrendingUp className="w-10 h-10 text-blue-500" />
                    </div>
                    <h3 className="text-lg font-medium text-slate-800">Trend Analysis</h3>
                    <p className="text-slate-500 mt-2 max-w-sm">
                        Historical view data collection is active.
                        Trends will appear here once we have 24h of data points.
                    </p>
                </div>

            </div>
        </div>
    );
};

// Sub-components
const KpiCard = ({ title, value, icon, alert }) => (
    <div className={`bg-white p-6 rounded-xl shadow-sm border ${alert ? 'border-orange-200 bg-orange-50' : 'border-slate-200'} transition-all hover:shadow-md`}>
        <div className="flex justify-between items-start">
            <div>
                <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">{title}</p>
                <h3 className="text-3xl font-bold text-slate-800 mt-2">{value}</h3>
            </div>
            <div className="p-2 bg-slate-50 rounded-lg">{icon}</div>
        </div>
    </div>
);

const StatusBadge = ({ status }) => {
    const colors = {
        healthy: 'bg-green-100 text-green-700',
        weak: 'bg-red-100 text-red-700',
        cooldown: 'bg-blue-100 text-blue-700',
        maxed: 'bg-gray-100 text-gray-700'
    };
    return (
        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${colors[status] || colors.weak}`}>
            {status.toUpperCase()}
        </span>
    );
};

export default Dashboard;

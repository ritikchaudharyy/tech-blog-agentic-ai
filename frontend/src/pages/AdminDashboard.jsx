import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  PenTool, 
  FileCode, 
  TrendingUp, 
  Shield,
  Search,
  Bell,
  MessageCircle,
  ChevronDown,
  Lock
} from 'lucide-react';
import AdminLayout from '../layouts/AdminLayout';
import { adminAPI } from '../api/admin.api';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const quickActions = [
    {
      title: 'Create New Article',
      description: 'Generate AI-powered content',
      icon: PenTool,
      action: () => navigate('/admin/create'),
      buttonText: 'Compose',
      gradient: 'from-blue-500 to-indigo-600',
      iconBg: 'bg-blue-500',
    },
    {
      title: 'AI Drafts',
      description: 'Review pending articles',
      icon: FileCode,
      action: () => navigate('/admin/content'),
      buttonText: 'View Drafts',
      gradient: 'from-purple-500 to-pink-600',
      iconBg: 'bg-purple-500',
      outlined: true,
    },
    {
      title: 'Traffic Analytics',
      description: 'Monitor performance metrics',
      icon: TrendingUp,
      action: () => navigate('/admin/analytics'),
      buttonText: 'View Stats',
      gradient: 'from-green-500 to-emerald-600',
      iconBg: 'bg-green-500',
      outlined: true,
    },
    {
      title: 'Manage Access',
      description: 'Control user permissions',
      icon: Shield,
      action: () => navigate('/admin/settings'),
      buttonText: 'Access Control',
      gradient: 'from-amber-500 to-orange-600',
      iconBg: 'bg-amber-500',
      outlined: true,
    },
  ];

  return (
    <AdminLayout>
      <div className="max-w-7xl mx-auto px-8 py-8 space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                type="text"
                placeholder="Search"
                className="w-80 h-11 pl-11 pr-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
              />
            </div>
          </div>

          <div className="flex items-center gap-4">
            <button className="relative p-2.5 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
              <MessageCircle className="w-5 h-5 text-slate-600 dark:text-slate-400" />
            </button>
            <button className="relative p-2.5 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
              <Bell className="w-5 h-5 text-slate-600 dark:text-slate-400" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            <div className="flex items-center gap-3 pl-4 border-l border-slate-200 dark:border-slate-700">
              <div className="w-9 h-9 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold text-sm shadow-lg">
                O
              </div>
              <ChevronDown className="w-4 h-4 text-slate-400" />
            </div>
          </div>
        </div>

        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-8 text-white shadow-xl shadow-blue-500/20">
          <div className="flex items-center gap-3 mb-3">
            <Lock className="w-5 h-5" />
            <span className="text-sm font-semibold bg-white/20 px-3 py-1 rounded-full">Owner</span>
          </div>
          <h1 className="text-3xl font-bold mb-2">
            Welcome back, Owner — Ready to Publish Knowledge
          </h1>
          <p className="text-blue-100 text-base">
            Manage your content and analytics in a secure AI-powered environment.
          </p>
        </div>

        {/* Quick Actions Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickActions.map((action, index) => {
            const Icon = action.icon;
            return (
              <div
                key={index}
                className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 hover:shadow-xl hover:shadow-slate-200/50 dark:hover:shadow-slate-900/50 transition-all duration-300 group"
              >
                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${action.gradient} flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform`}>
                  <Icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">
                  {action.title}
                </h3>
                <p className="text-sm text-slate-500 dark:text-slate-400 mb-6">
                  {action.description}
                </p>
                <button
                  onClick={action.action}
                  className={`w-full h-11 rounded-xl font-semibold text-sm transition-all duration-200 ${
                    action.outlined
                      ? 'border-2 border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:border-blue-500 hover:text-blue-600 dark:hover:border-blue-500 dark:hover:text-blue-400'
                      : 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/30 hover:shadow-xl hover:shadow-blue-500/40'
                  }`}
                >
                  {action.buttonText}
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </AdminLayout>
  );
};

export default AdminDashboard;
import { apiClient } from './client';

export const adminAPI = {
  getMetrics: async () => {
    return apiClient.get('/api/admin/metrics');
  },

  getTraffic: async () => {
    return apiClient.get('/api/admin/traffic');
  },

  getArticles: async () => {
    return apiClient.get('/api/admin/articles');
  },

  autoPublish: async (payload) => {
    return apiClient.post('/api/admin/auto-publish', payload);
  },

  autoPublishTrending: async () => {
    return apiClient.post('/api/admin/auto-publish/trending', {});
  },
};

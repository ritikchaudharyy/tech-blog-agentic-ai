import { apiClient } from './client';

export const userAPI = {
  getTrending: async () => {
    return apiClient.get('/api/articles/trending');
  },

  getArticleById: async (id) => {
    return apiClient.get(`/api/articles/${id}`);
  },

  searchArticles: async (keyword) => {
    return apiClient.get(`/api/articles/search/${keyword}`);
  },
};

import { apiClient } from './client';

/**
 * User API Module
 * Centralized API calls for public user operations
 */
export const userAPI = {
  /**
   * Get trending articles
   * @returns {Promise<Array>} List of trending articles
   */
  getTrending: async () => {
    return apiClient.get('/api/articles/trending');
  },

  /**
   * Get all public articles
   * @returns {Promise<Array>} List of all published articles
   */
  getAllArticles: async () => {
    return apiClient.get('/api/articles');
  },

  /**
   * Get article by ID
   * @param {number|string} id - Article ID
   * @returns {Promise<Object>} Article details
   */
  getArticleById: async (id) => {
    return apiClient.get(`/api/articles/${id}`);
  },

  /**
   * Search articles by keyword
   * @param {string} keyword - Search keyword
   * @returns {Promise<Array>} Matching articles
   */
  searchArticles: async (keyword) => {
    return apiClient.get(`/api/articles/search/${encodeURIComponent(keyword)}`);
  },

  /**
   * Increment article view count
   * @param {number|string} id - Article ID
   * @returns {Promise<Object>} Updated view count
   */
  incrementViews: async (id) => {
    return apiClient.post(`/api/articles/${id}/view`, {});
  },

  /**
   * Get articles by category
   * @param {string} category - Category name
   * @returns {Promise<Array>} Articles in category
   */
  getByCategory: async (category) => {
    return apiClient.get(`/api/articles/category/${encodeURIComponent(category)}`);
  },
};
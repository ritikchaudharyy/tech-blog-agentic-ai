import { apiClient } from './client';

/**
 * Admin API Module
 * Centralized API calls for admin dashboard operations
 */
export const adminAPI = {
  /**
   * Get admin dashboard metrics
   * @returns {Promise<Object>} Metrics data including user count, article count, etc.
   */
  getMetrics: async () => {
    return apiClient.get('/api/admin/metrics');
  },

  /**
   * Get traffic analytics data
   * @returns {Promise<Object>} Traffic data with timestamps and view counts
   */
  getTraffic: async () => {
    return apiClient.get('/api/admin/traffic');
  },

  /**
   * Get all articles with admin details
   * @returns {Promise<Array>} List of articles with metadata
   */
  getArticles: async () => {
    return apiClient.get('/api/admin/articles');
  },

  /**
   * Trigger auto-publish workflow
   * @param {Object} payload - Publication configuration
   * @param {string} payload.topic - Topic to generate content about
   * @param {string} payload.platform - Target platform (blogger/wordpress)
   * @returns {Promise<Object>} Publication result
   */
  autoPublish: async (payload) => {
    return apiClient.post('/api/admin/auto-publish', payload);
  },

  /**
   * Auto-publish trending topic
   * @returns {Promise<Object>} Publication result for trending content
   */
  autoPublishTrending: async () => {
    return apiClient.post('/api/admin/auto-publish/trending', {});
  },

  /**
   * Delete an article
   * @param {number} articleId - ID of article to delete
   * @returns {Promise<Object>} Deletion confirmation
   */
  deleteArticle: async (articleId) => {
    return apiClient.delete(`/api/admin/articles/${articleId}`);
  },

  /**
   * Update article metadata
   * @param {number} articleId - ID of article to update
   * @param {Object} data - Updated article data
   * @returns {Promise<Object>} Updated article
   */
  updateArticle: async (articleId, data) => {
    return apiClient.put(`/api/admin/articles/${articleId}`, data);
  },
};
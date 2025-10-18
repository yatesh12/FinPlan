import api from './index';

export const portfolioAPI = {
  // Get portfolio allocations for dashboard
  getPortfolioAllocations: async () => {
    try {
      const response = await api.get('/api/portfolio/allocations');
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching portfolio allocations:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch portfolio allocations'
      };
    }
  },

  // Get full portfolio prediction
  getPortfolioPrediction: async () => {
    try {
      const response = await api.get('/api/portfolio/predict');
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching portfolio prediction:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch portfolio prediction'
      };
    }
  },

  // Submit portfolio feedback
  submitPortfolioFeedback: async (feedbackData) => {
    try {
      const response = await api.post('/api/portfolio/feedback', feedbackData);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error submitting portfolio feedback:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to submit feedback'
      };
    }
  }
};

export default portfolioAPI;
import api from './index';

// Profile API calls
export const profileAPI = {
  // Get user profile
  getProfile: async () => {
    const response = await api.get('/api/profile/');
    return response.data;
  },

  // Update user profile (FastAPI uses POST for both create and update)
  updateProfile: async (profileData) => {
    const response = await api.post('/api/profile/', profileData);
    return response.data;
  },

  // Create user profile (same as update in FastAPI)
  createProfile: async (profileData) => {
    const response = await api.post('/api/profile/', profileData);
    return response.data;
  },

  // Get user's financial goals
  getGoals: async () => {
    const response = await api.get('/api/profile/goals');
    return response.data;
  },

  // Add financial goal
  addGoal: async (goalData) => {
    const response = await api.post('/api/profile/goals', goalData);
    return response.data;
  },

  // Update financial goal
  updateGoal: async (goalId, goalData) => {
    const response = await api.put(`/api/profile/goals/${goalId}`, goalData);
    return response.data;
  },

  // Delete financial goal
  deleteGoal: async (goalId) => {
    const response = await api.delete(`/api/profile/goals/${goalId}`);
    return response.data;
  }
};

export default profileAPI;
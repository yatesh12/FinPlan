import api from './index';

// User API calls
export const userAPI = {
  // Get current user information
  getCurrentUser: async () => {
    const response = await api.get('/api/me/');
    return response.data;
  },

  // Check if user's profile is completed
  checkProfileStatus: async () => {
    const response = await api.get('/api/me/');
    return {
      profileCompleted: response.data.profileCompleted,
      user: response.data.account
    };
  }
};

export default userAPI;
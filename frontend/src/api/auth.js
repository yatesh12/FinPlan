import api from './index';

// Authentication API calls
export const authAPI = {
  // User registration
  signup: async (userData) => {
    const response = await api.post('/auth/signup', userData);
    return response.data;
  },

  // User login
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    const { accessToken } = response.data;
    
    // Store access token in localStorage
    if (accessToken) {
      localStorage.setItem('accessToken', accessToken);
    }
    
    return response.data;
  },

  // Logout
  logout: async () => {
    try {
      await api.post('/auth/logout');
    } finally {
      // Always remove token from localStorage
      localStorage.removeItem('accessToken');
    }
  },

  // Refresh access token
  refreshToken: async () => {
    const response = await api.post('/auth/refresh');
    const { accessToken } = response.data;
    
    if (accessToken) {
      localStorage.setItem('accessToken', accessToken);
    }
    
    return response.data;
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('accessToken');
  },

  // Get current access token
  getAccessToken: () => {
    return localStorage.getItem('accessToken');
  }
};

export default authAPI;
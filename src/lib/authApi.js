/**
 * Authentication API client for backend communication
 */

const API_BASE_URL = typeof window !== 'undefined' && window.location.hostname !== 'localhost'
  ? 'https://your-backend-url.com'
  : 'http://localhost:8000';

export const authApi = {
  /**
   * Sign up a new user
   */
  signup: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Signup failed');
    }

    return response.json();
  },

  /**
   * Sign in existing user
   */
  signin: async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/signin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Signin failed');
    }

    return response.json();
  },

  /**
   * Get current user profile
   */
  getCurrentUser: async (token) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!response.ok) {
      throw new Error('Failed to get user profile');
    }

    return response.json();
  },

  /**
   * Submit background questionnaire
   */
  submitQuestionnaire: async (token, questionnaireData) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/questionnaire`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(questionnaireData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to submit questionnaire');
    }

    return response.json();
  },

  /**
   * Get personalized dashboard
   */
  getDashboard: async (token) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/dashboard`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!response.ok) {
      throw new Error('Failed to get dashboard');
    }

    return response.json();
  }
};

/**
 * Token storage utilities
 */
export const tokenStorage = {
  get: () => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('auth_token');
  },

  set: (token) => {
    if (typeof window === 'undefined') return;
    localStorage.setItem('auth_token', token);
  },

  remove: () => {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('auth_token');
  }
};

/**
 * User storage utilities
 */
export const userStorage = {
  get: () => {
    if (typeof window === 'undefined') return null;
    const user = localStorage.getItem('auth_user');
    return user ? JSON.parse(user) : null;
  },

  set: (user) => {
    if (typeof window === 'undefined') return;
    localStorage.setItem('auth_user', JSON.stringify(user));
  },

  remove: () => {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('auth_user');
  }
};

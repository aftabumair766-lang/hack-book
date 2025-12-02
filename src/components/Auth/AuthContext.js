/**
 * Authentication Context Provider
 * Manages global authentication state
 */
import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi, tokenStorage, userStorage } from '../../lib/authApi';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Initialize auth state from localStorage
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = tokenStorage.get();
      const storedUser = userStorage.get();

      if (storedToken && storedUser) {
        try {
          // Verify token is still valid by fetching user
          const currentUser = await authApi.getCurrentUser(storedToken);
          setToken(storedToken);
          setUser(currentUser);
          setIsAuthenticated(true);
        } catch (error) {
          // Token invalid, clear storage
          console.error('Token validation failed:', error);
          tokenStorage.remove();
          userStorage.remove();
        }
      }

      setLoading(false);
    };

    initAuth();
  }, []);

  const signup = async (userData) => {
    try {
      const response = await authApi.signup(userData);
      const { access_token, user: newUser } = response;

      // Store auth data
      tokenStorage.set(access_token);
      userStorage.set(newUser);

      setToken(access_token);
      setUser(newUser);
      setIsAuthenticated(true);

      return { success: true, user: newUser };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const signin = async (credentials) => {
    try {
      const response = await authApi.signin(credentials);
      const { access_token, user: existingUser } = response;

      // Store auth data
      tokenStorage.set(access_token);
      userStorage.set(existingUser);

      setToken(access_token);
      setUser(existingUser);
      setIsAuthenticated(true);

      return { success: true, user: existingUser };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const signout = () => {
    tokenStorage.remove();
    userStorage.remove();
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
  };

  const submitQuestionnaire = async (questionnaireData) => {
    if (!token) {
      return { success: false, error: 'Not authenticated' };
    }

    try {
      await authApi.submitQuestionnaire(token, questionnaireData);

      // Update user to reflect completed questionnaire
      const updatedUser = { ...user, has_completed_questionnaire: true };
      setUser(updatedUser);
      userStorage.set(updatedUser);

      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const getDashboard = async () => {
    if (!token) {
      throw new Error('Not authenticated');
    }

    return authApi.getDashboard(token);
  };

  const value = {
    user,
    token,
    loading,
    isAuthenticated,
    signup,
    signin,
    signout,
    submitQuestionnaire,
    getDashboard
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

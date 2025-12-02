import React from 'react';
import Chatbot from '../components/Chatbot';
import { AuthProvider } from '../components/Auth/AuthContext';

// This component wraps the entire app
export default function Root({children}) {
  return (
    <AuthProvider>
      {children}
      <Chatbot />
    </AuthProvider>
  );
}

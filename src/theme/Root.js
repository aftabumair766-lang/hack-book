import React from 'react';
import Chatbot from '../components/Chatbot';

// This component wraps the entire app
export default function Root({children}) {
  return (
    <>
      {children}
      <Chatbot />
    </>
  );
}

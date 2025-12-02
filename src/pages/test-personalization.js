import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../components/Auth/AuthContext';
import PersonalizeButton from '../components/PersonalizeButton';

export default function TestPersonalization() {
  const { user, isAuthenticated } = useAuth();
  const [personalizedData, setPersonalizedData] = useState(null);

  const handlePersonalize = (data) => {
    console.log('Personalization data received:', data);
    setPersonalizedData(data);
  };

  return (
    <Layout title="Test Personalization">
      <div style={{ maxWidth: '1200px', margin: '2rem auto', padding: '0 2rem' }}>
        <h1>🧪 Personalization System Test Page</h1>

        <div style={{
          padding: '1.5rem',
          background: 'rgba(0, 217, 255, 0.1)',
          border: '1px solid #00d9ff',
          borderRadius: '8px',
          marginBottom: '2rem'
        }}>
          <h2>Authentication Status</h2>
          <p>
            <strong>Logged In:</strong> {isAuthenticated ? '✅ Yes' : '❌ No'}
          </p>
          {user && (
            <>
              <p><strong>Email:</strong> {user.email}</p>
              <p><strong>Questionnaire Completed:</strong> {user.has_completed_questionnaire ? '✅ Yes' : '❌ No'}</p>
            </>
          )}
          {!isAuthenticated && (
            <p style={{ color: '#ff4444' }}>
              Please <a href="/signup">sign up</a> or <a href="/signin">sign in</a> to test personalization.
            </p>
          )}
          {isAuthenticated && !user?.has_completed_questionnaire && (
            <p style={{ color: '#ffc107' }}>
              Please complete the <a href="/questionnaire">questionnaire</a> to enable personalization.
            </p>
          )}
        </div>

        <div style={{
          padding: '1.5rem',
          background: 'rgba(0, 217, 255, 0.05)',
          border: '1px solid #00d9ff',
          borderRadius: '8px',
          marginBottom: '2rem'
        }}>
          <h2>Personalization Test</h2>
          <PersonalizeButton
            chapterId="chapter-01"
            onPersonalize={handlePersonalize}
          />
        </div>

        {personalizedData && (
          <div style={{
            padding: '1.5rem',
            background: 'rgba(0, 255, 100, 0.05)',
            border: '1px solid #0f0',
            borderRadius: '8px',
            marginBottom: '2rem'
          }}>
            <h2>✅ Personalization Result</h2>

            <h3>Profile Summary:</h3>
            <pre style={{ background: '#1e1e1e', padding: '1rem', borderRadius: '4px', overflow: 'auto' }}>
              {JSON.stringify(personalizedData.user_profile_summary, null, 2)}
            </pre>

            <h3>Transformations Applied:</h3>
            <ul>
              {personalizedData.transformations_applied.map((t, i) => (
                <li key={i}>{t}</li>
              ))}
            </ul>

            <h3>Content Length:</h3>
            <p>Original: {personalizedData.original_length} characters</p>
            <p>Personalized: {personalizedData.personalized_length} characters</p>

            <h3>Personalized Content Preview (first 500 chars):</h3>
            <pre style={{ background: '#1e1e1e', padding: '1rem', borderRadius: '4px', overflow: 'auto', whiteSpace: 'pre-wrap' }}>
              {personalizedData.personalized_content.substring(0, 500)}...
            </pre>
          </div>
        )}

        <div style={{
          padding: '1.5rem',
          background: 'rgba(136, 136, 136, 0.1)',
          border: '1px solid #666',
          borderRadius: '8px'
        }}>
          <h2>Test Instructions</h2>
          <ol>
            <li>Make sure you're signed in</li>
            <li>Complete the background questionnaire if you haven't</li>
            <li>Click the "Personalize This Chapter" button above</li>
            <li>Check the result below</li>
            <li>Open browser console (F12) for detailed logs</li>
          </ol>
        </div>
      </div>
    </Layout>
  );
}

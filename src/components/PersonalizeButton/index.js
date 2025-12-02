import React, { useState } from 'react';
import { useAuth } from '../Auth/AuthContext';
import styles from './styles.module.css';

const API_BASE_URL = typeof window !== 'undefined' && window.location.hostname !== 'localhost'
  ? 'https://your-backend-url.com'
  : 'http://localhost:8000';

export default function PersonalizeButton({ chapterId, onPersonalize }) {
  const { user, token, isAuthenticated } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [personalized, setPersonalized] = useState(false);

  const handlePersonalize = async () => {
    if (!isAuthenticated || !token) {
      setError('Please sign in to personalize content');
      return;
    }

    if (!user?.has_completed_questionnaire) {
      setError('Please complete the background questionnaire first');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE_URL}/api/personalize/chapter`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          chapter_id: chapterId
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to personalize content');
      }

      const data = await response.json();

      // Call parent callback with personalized content
      if (onPersonalize) {
        onPersonalize(data);
      }

      setPersonalized(true);
    } catch (err) {
      setError(err.message);
      console.error('Personalization error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Don't show button if not authenticated
  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className={styles.personalizeContainer}>
      {!personalized ? (
        <button
          onClick={handlePersonalize}
          disabled={loading}
          className={styles.personalizeButton}
        >
          {loading ? (
            <>
              <span className={styles.spinner}></span>
              Personalizing...
            </>
          ) : (
            <>
              <span className={styles.icon}>✨</span>
              Personalize This Chapter
            </>
          )}
        </button>
      ) : (
        <div className={styles.successMessage}>
          <span className={styles.checkIcon}>✓</span>
          Content personalized for your profile!
        </div>
      )}

      {error && (
        <div className={styles.error}>
          {error}
          {error.includes('questionnaire') && (
            <a href="/questionnaire" className={styles.errorLink}>
              Complete questionnaire →
            </a>
          )}
        </div>
      )}

      {!user?.has_completed_questionnaire && isAuthenticated && (
        <div className={styles.hint}>
          💡 Complete your <a href="/questionnaire">background questionnaire</a> to enable personalization
        </div>
      )}
    </div>
  );
}

import React, { useState } from 'react';
import { useAuth } from '../Auth/AuthContext';
import PersonalizeButton from '../PersonalizeButton';
import ReactMarkdown from 'react-markdown';
import styles from './styles.module.css';

export default function PersonalizedChapter({ chapterId, children }) {
  const { isAuthenticated } = useAuth();
  const [personalizedData, setPersonalizedData] = useState(null);

  const handlePersonalize = (data) => {
    setPersonalizedData(data);
  };

  const handleReset = () => {
    setPersonalizedData(null);
  };

  return (
    <div className={styles.chapterContainer}>
      {/* Only show button if authenticated */}
      {isAuthenticated && (
        <PersonalizeButton
          chapterId={chapterId}
          onPersonalize={handlePersonalize}
        />
      )}

      {/* Show personalized content or original */}
      {personalizedData ? (
        <div className={styles.personalizedContent}>
          {/* Profile Summary */}
          <div className={styles.profileSummary}>
            <h3>📊 Your Profile</h3>
            <div className={styles.profileGrid}>
              <div>
                <strong>Software:</strong> {personalizedData.user_profile_summary.software_experience}
              </div>
              <div>
                <strong>Hardware:</strong> {personalizedData.user_profile_summary.hardware_experience}
              </div>
              <div>
                <strong>Language:</strong> {personalizedData.user_profile_summary.preferred_language}
              </div>
              <div>
                <strong>Interest:</strong> {personalizedData.user_profile_summary.primary_interest}
              </div>
            </div>
          </div>

          {/* Transformations Applied */}
          <div className={styles.transformations}>
            <h4>✨ Transformations Applied:</h4>
            <ul>
              {personalizedData.transformations_applied.map((t, i) => (
                <li key={i}>{t}</li>
              ))}
            </ul>
          </div>

          {/* Personalized Content */}
          <div className={styles.content}>
            <ReactMarkdown>{personalizedData.personalized_content}</ReactMarkdown>
          </div>

          {/* Reset Button */}
          <button onClick={handleReset} className={styles.resetButton}>
            ← View Original Content
          </button>
        </div>
      ) : (
        <div className={styles.originalContent}>
          {children}
        </div>
      )}
    </div>
  );
}

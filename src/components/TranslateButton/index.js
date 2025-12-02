import React, { useState } from 'react';
import { useAuth } from '../Auth/AuthContext';
import styles from './styles.module.css';

const API_BASE_URL = typeof window !== 'undefined' && window.location.hostname !== 'localhost'
  ? 'https://your-backend-url.com'
  : 'http://localhost:8000';

export default function TranslateButton({ chapterId, onTranslate }) {
  const { isAuthenticated, token } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [translated, setTranslated] = useState(false);
  const [showLanguages, setShowLanguages] = useState(false);

  const languages = [
    { code: 'urdu', name: 'Urdu', native: 'اردو', flag: '🇵🇰' },
    { code: 'arabic', name: 'Arabic', native: 'العربية', flag: '🇸🇦' },
    { code: 'spanish', name: 'Spanish', native: 'Español', flag: '🇪🇸' },
    { code: 'french', name: 'French', native: 'Français', flag: '🇫🇷' },
    { code: 'german', name: 'German', native: 'Deutsch', flag: '🇩🇪' },
    { code: 'hindi', name: 'Hindi', native: 'हिन्दी', flag: '🇮🇳' },
    { code: 'chinese', name: 'Chinese', native: '中文', flag: '🇨🇳' },
  ];

  const handleTranslate = async (languageCode) => {
    if (!isAuthenticated || !token) {
      setError('Please sign in to translate content');
      return;
    }

    setLoading(true);
    setError('');
    setShowLanguages(false);

    try {
      const response = await fetch(`${API_BASE_URL}/api/translate/chapter`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          chapter_id: chapterId,
          target_language: languageCode
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Translation failed');
      }

      const data = await response.json();

      // Call parent callback with translated content
      if (onTranslate) {
        onTranslate(data);
      }

      setTranslated(true);
    } catch (err) {
      setError(err.message);
      console.error('Translation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setTranslated(false);
    if (onTranslate) {
      onTranslate(null); // Signal to show original content
    }
  };

  // Don't show button if not authenticated
  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className={styles.translateContainer}>
      {!translated ? (
        <div className={styles.buttonGroup}>
          <button
            onClick={() => setShowLanguages(!showLanguages)}
            disabled={loading}
            className={styles.translateButton}
          >
            {loading ? (
              <>
                <span className={styles.spinner}></span>
                Translating...
              </>
            ) : (
              <>
                <span className={styles.icon}>🌍</span>
                Translate to Urdu / Other Languages
              </>
            )}
          </button>

          {showLanguages && !loading && (
            <div className={styles.languageDropdown}>
              <div className={styles.dropdownHeader}>Select Language:</div>
              {languages.map((lang) => (
                <button
                  key={lang.code}
                  onClick={() => handleTranslate(lang.code)}
                  className={styles.languageOption}
                >
                  <span className={styles.flag}>{lang.flag}</span>
                  <span className={styles.native}>{lang.native}</span>
                  <span className={styles.english}>({lang.name})</span>
                </button>
              ))}
            </div>
          )}
        </div>
      ) : (
        <div className={styles.translatedBanner}>
          <span className={styles.checkIcon}>✓</span>
          Content translated successfully!
          <button onClick={handleReset} className={styles.resetButton}>
            View Original (English)
          </button>
        </div>
      )}

      {error && (
        <div className={styles.error}>
          {error}
        </div>
      )}
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import { useAuth } from '../components/Auth/AuthContext';
import { useHistory } from '@docusaurus/router';
import Layout from '@theme/Layout';

export default function DashboardPage() {
  const { user, getDashboard, signout } = useAuth();
  const history = useHistory();
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadDashboard = async () => {
      if (!user) {
        history.push('/signin');
        return;
      }

      if (!user.has_completed_questionnaire) {
        history.push('/questionnaire');
        return;
      }

      try {
        const data = await getDashboard();
        setDashboard(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, [user, getDashboard, history]);

  const handleSignout = () => {
    signout();
    history.push('/');
  };

  if (loading) {
    return (
      <Layout title="Dashboard">
        <div style={{ textAlign: 'center', padding: '4rem', color: '#00d9ff' }}>
          <h2>Loading your personalized dashboard...</h2>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout title="Dashboard">
        <div style={{ textAlign: 'center', padding: '4rem', color: '#ff4444' }}>
          <h2>Error loading dashboard</h2>
          <p>{error}</p>
        </div>
      </Layout>
    );
  }

  const cardStyle = {
    background: 'rgba(0, 217, 255, 0.05)',
    border: '1px solid #00d9ff',
    borderRadius: '8px',
    padding: '1.5rem',
    marginBottom: '1.5rem',
    boxShadow: '0 0 15px rgba(0, 217, 255, 0.1)'
  };

  const headingStyle = {
    color: '#00ffff',
    marginBottom: '1rem',
    textTransform: 'uppercase',
    letterSpacing: '2px',
    fontSize: '1.2rem'
  };

  return (
    <Layout title="Your Personalized Dashboard">
      <div style={{
        maxWidth: '1200px',
        margin: '2rem auto',
        padding: '0 2rem'
      }}>
        {/* Header with Welcome and Signout */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '2rem',
          padding: '1.5rem',
          background: 'linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 136, 255, 0.1) 100%)',
          border: '1px solid #00d9ff',
          borderRadius: '8px'
        }}>
          <div>
            <h1 style={{
              color: '#00ffff',
              margin: '0 0 0.5rem 0',
              textTransform: 'uppercase',
              letterSpacing: '2px'
            }}>
              {dashboard?.welcome_message || 'Welcome to Your Dashboard'}
            </h1>
            <p style={{ color: '#888', margin: 0 }}>
              Logged in as: <strong style={{ color: '#00d9ff' }}>{user?.email}</strong>
            </p>
          </div>
          <button
            onClick={handleSignout}
            style={{
              padding: '0.75rem 1.5rem',
              background: 'rgba(255, 68, 68, 0.2)',
              color: '#ff4444',
              border: '1px solid #ff4444',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold',
              textTransform: 'uppercase',
              letterSpacing: '1px',
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              e.target.style.background = 'rgba(255, 68, 68, 0.3)';
              e.target.style.boxShadow = '0 0 10px rgba(255, 68, 68, 0.5)';
            }}
            onMouseLeave={(e) => {
              e.target.style.background = 'rgba(255, 68, 68, 0.2)';
              e.target.style.boxShadow = 'none';
            }}
          >
            Sign Out
          </button>
        </div>

        {/* Skill Level Badge */}
        {dashboard?.skill_level_badge && (
          <div style={{
            ...cardStyle,
            textAlign: 'center',
            background: 'linear-gradient(135deg, rgba(0, 217, 255, 0.15) 0%, rgba(0, 136, 255, 0.15) 100%)'
          }}>
            <h2 style={{ color: '#00ffff', margin: 0 }}>
              {dashboard.skill_level_badge}
            </h2>
          </div>
        )}

        {/* Recommended Chapters */}
        {dashboard?.recommended_chapters && dashboard.recommended_chapters.length > 0 && (
          <div style={cardStyle}>
            <h2 style={headingStyle}>Recommended Chapters</h2>
            <div style={{ display: 'grid', gap: '1rem' }}>
              {dashboard.recommended_chapters.map((chapter, idx) => (
                <div
                  key={idx}
                  style={{
                    padding: '1rem',
                    background: 'rgba(0, 217, 255, 0.08)',
                    borderLeft: '4px solid #00d9ff',
                    borderRadius: '4px'
                  }}
                >
                  <h3 style={{ color: '#00d9ff', margin: '0 0 0.5rem 0' }}>
                    {chapter.title}
                  </h3>
                  <p style={{ color: '#e0e0e0', margin: '0 0 0.5rem 0' }}>
                    {chapter.description}
                  </p>
                  {chapter.priority && (
                    <span style={{
                      display: 'inline-block',
                      padding: '0.25rem 0.75rem',
                      background: 'rgba(0, 217, 255, 0.2)',
                      color: '#00d9ff',
                      borderRadius: '12px',
                      fontSize: '0.85rem',
                      fontWeight: 'bold',
                      textTransform: 'uppercase'
                    }}>
                      Priority: {chapter.priority}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Learning Path */}
        {dashboard?.learning_path && dashboard.learning_path.length > 0 && (
          <div style={cardStyle}>
            <h2 style={headingStyle}>Your Learning Path</h2>
            <ol style={{ color: '#e0e0e0', lineHeight: '2', margin: 0, paddingLeft: '1.5rem' }}>
              {dashboard.learning_path.map((step, idx) => (
                <li key={idx} style={{ marginBottom: '0.5rem' }}>
                  {step}
                </li>
              ))}
            </ol>
          </div>
        )}

        {/* Quick Tips */}
        {dashboard?.quick_tips && dashboard.quick_tips.length > 0 && (
          <div style={cardStyle}>
            <h2 style={headingStyle}>Quick Tips</h2>
            <div style={{ display: 'grid', gap: '1rem' }}>
              {dashboard.quick_tips.map((tip, idx) => (
                <div
                  key={idx}
                  style={{
                    padding: '1rem',
                    background: 'rgba(0, 217, 255, 0.08)',
                    borderRadius: '4px',
                    color: '#e0e0e0'
                  }}
                >
                  <span style={{ color: '#00d9ff', fontWeight: 'bold', marginRight: '0.5rem' }}>
                    {idx + 1}.
                  </span>
                  {tip}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Suggested Exercises */}
        {dashboard?.suggested_exercises && dashboard.suggested_exercises.length > 0 && (
          <div style={cardStyle}>
            <h2 style={headingStyle}>Suggested Exercises</h2>
            <div style={{ display: 'grid', gap: '1rem' }}>
              {dashboard.suggested_exercises.map((exercise, idx) => (
                <div
                  key={idx}
                  style={{
                    padding: '1.5rem',
                    background: 'rgba(0, 217, 255, 0.08)',
                    border: '1px solid rgba(0, 217, 255, 0.3)',
                    borderRadius: '6px'
                  }}
                >
                  <h3 style={{ color: '#00d9ff', margin: '0 0 0.75rem 0' }}>
                    {exercise.title}
                  </h3>
                  <p style={{ color: '#e0e0e0', margin: '0 0 0.75rem 0' }}>
                    {exercise.description}
                  </p>
                  {exercise.difficulty && (
                    <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                      <span style={{
                        padding: '0.25rem 0.75rem',
                        background: exercise.difficulty === 'easy' ? 'rgba(0, 255, 100, 0.2)' :
                                   exercise.difficulty === 'medium' ? 'rgba(255, 200, 0, 0.2)' :
                                   'rgba(255, 68, 68, 0.2)',
                        color: exercise.difficulty === 'easy' ? '#0f0' :
                               exercise.difficulty === 'medium' ? '#fc0' :
                               '#ff4444',
                        borderRadius: '12px',
                        fontSize: '0.85rem',
                        fontWeight: 'bold',
                        textTransform: 'uppercase'
                      }}>
                        {exercise.difficulty}
                      </span>
                      {exercise.estimated_time && (
                        <span style={{
                          padding: '0.25rem 0.75rem',
                          background: 'rgba(0, 217, 255, 0.2)',
                          color: '#00d9ff',
                          borderRadius: '12px',
                          fontSize: '0.85rem'
                        }}>
                          {exercise.estimated_time}
                        </span>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Quick Links */}
        <div style={{
          ...cardStyle,
          textAlign: 'center',
          background: 'rgba(0, 217, 255, 0.05)'
        }}>
          <h2 style={headingStyle}>Quick Links</h2>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <a
              href="/docs/chapter-01"
              style={{
                padding: '0.75rem 1.5rem',
                background: 'linear-gradient(135deg, #00d9ff 0%, #0088ff 100%)',
                color: '#000',
                textDecoration: 'none',
                borderRadius: '4px',
                fontWeight: 'bold',
                textTransform: 'uppercase',
                letterSpacing: '1px',
                transition: 'all 0.3s ease'
              }}
            >
              Start Learning
            </a>
            <a
              href="/questionnaire"
              style={{
                padding: '0.75rem 1.5rem',
                background: 'rgba(0, 217, 255, 0.2)',
                color: '#00d9ff',
                border: '1px solid #00d9ff',
                textDecoration: 'none',
                borderRadius: '4px',
                fontWeight: 'bold',
                textTransform: 'uppercase',
                letterSpacing: '1px',
                transition: 'all 0.3s ease'
              }}
            >
              Update Questionnaire
            </a>
          </div>
        </div>
      </div>
    </Layout>
  );
}

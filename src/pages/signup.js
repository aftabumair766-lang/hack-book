import React, { useState } from 'react';
import { useAuth } from '../components/Auth/AuthContext';
import { useHistory } from '@docusaurus/router';
import Layout from '@theme/Layout';

export default function SignupPage() {
  const { signup } = useAuth();
  const history = useHistory();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await signup(formData);

    if (result.success) {
      // Redirect to questionnaire if not completed
      if (!result.user.has_completed_questionnaire) {
        history.push('/questionnaire');
      } else {
        history.push('/dashboard');
      }
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  return (
    <Layout title="Sign Up" description="Create your account">
      <div style={{
        maxWidth: '500px',
        margin: '4rem auto',
        padding: '2rem',
        background: 'rgba(0, 217, 255, 0.05)',
        border: '1px solid #00d9ff',
        borderRadius: '8px',
        boxShadow: '0 0 20px rgba(0, 217, 255, 0.2)'
      }}>
        <h1 style={{
          color: '#00ffff',
          textAlign: 'center',
          marginBottom: '2rem',
          textTransform: 'uppercase',
          letterSpacing: '2px'
        }}>
          Create Account
        </h1>

        {error && (
          <div style={{
            color: '#ff4444',
            background: 'rgba(255, 68, 68, 0.1)',
            border: '1px solid #ff4444',
            padding: '1rem',
            marginBottom: '1.5rem',
            borderRadius: '4px'
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{
              display: 'block',
              color: '#00d9ff',
              marginBottom: '0.5rem',
              fontWeight: 'bold',
              textTransform: 'uppercase',
              fontSize: '0.9rem',
              letterSpacing: '1px'
            }}>
              Full Name
            </label>
            <input
              type="text"
              value={formData.full_name}
              onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
              required
              style={{
                width: '100%',
                padding: '0.75rem',
                background: 'rgba(0, 217, 255, 0.1)',
                border: '1px solid #00d9ff',
                borderRadius: '4px',
                color: '#e0e0e0',
                fontSize: '1rem',
                outline: 'none',
                transition: 'all 0.3s ease'
              }}
              onFocus={(e) => e.target.style.boxShadow = '0 0 10px rgba(0, 217, 255, 0.5)'}
              onBlur={(e) => e.target.style.boxShadow = 'none'}
            />
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{
              display: 'block',
              color: '#00d9ff',
              marginBottom: '0.5rem',
              fontWeight: 'bold',
              textTransform: 'uppercase',
              fontSize: '0.9rem',
              letterSpacing: '1px'
            }}>
              Email
            </label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
              style={{
                width: '100%',
                padding: '0.75rem',
                background: 'rgba(0, 217, 255, 0.1)',
                border: '1px solid #00d9ff',
                borderRadius: '4px',
                color: '#e0e0e0',
                fontSize: '1rem',
                outline: 'none',
                transition: 'all 0.3s ease'
              }}
              onFocus={(e) => e.target.style.boxShadow = '0 0 10px rgba(0, 217, 255, 0.5)'}
              onBlur={(e) => e.target.style.boxShadow = 'none'}
            />
          </div>

          <div style={{ marginBottom: '2rem' }}>
            <label style={{
              display: 'block',
              color: '#00d9ff',
              marginBottom: '0.5rem',
              fontWeight: 'bold',
              textTransform: 'uppercase',
              fontSize: '0.9rem',
              letterSpacing: '1px'
            }}>
              Password (min 8 characters)
            </label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
              minLength={8}
              style={{
                width: '100%',
                padding: '0.75rem',
                background: 'rgba(0, 217, 255, 0.1)',
                border: '1px solid #00d9ff',
                borderRadius: '4px',
                color: '#e0e0e0',
                fontSize: '1rem',
                outline: 'none',
                transition: 'all 0.3s ease'
              }}
              onFocus={(e) => e.target.style.boxShadow = '0 0 10px rgba(0, 217, 255, 0.5)'}
              onBlur={(e) => e.target.style.boxShadow = 'none'}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '1rem',
              background: loading ? '#555' : 'linear-gradient(135deg, #00d9ff 0%, #0088ff 100%)',
              color: '#000',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontSize: '1rem',
              fontWeight: 'bold',
              textTransform: 'uppercase',
              letterSpacing: '2px',
              transition: 'all 0.3s ease',
              opacity: loading ? 0.6 : 1
            }}
            onMouseEnter={(e) => {
              if (!loading) {
                e.target.style.boxShadow = '0 0 20px rgba(0, 217, 255, 0.6)';
                e.target.style.transform = 'translateY(-2px)';
              }
            }}
            onMouseLeave={(e) => {
              e.target.style.boxShadow = 'none';
              e.target.style.transform = 'translateY(0)';
            }}
          >
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        <p style={{
          marginTop: '2rem',
          textAlign: 'center',
          color: '#888'
        }}>
          Already have an account?{' '}
          <a
            href="/signin"
            style={{
              color: '#00d9ff',
              textDecoration: 'none',
              fontWeight: 'bold'
            }}
            onMouseEnter={(e) => e.target.style.textDecoration = 'underline'}
            onMouseLeave={(e) => e.target.style.textDecoration = 'none'}
          >
            Sign In
          </a>
        </p>
      </div>
    </Layout>
  );
}

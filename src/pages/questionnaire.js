import React, { useState, useEffect } from 'react';
import { useAuth } from '../components/Auth/AuthContext';
import { useHistory } from '@docusaurus/router';
import Layout from '@theme/Layout';

export default function QuestionnairePage() {
  const { user, submitQuestionnaire } = useAuth();
  const history = useHistory();
  const [formData, setFormData] = useState({
    software_experience: 'beginner',
    years_coding: '',
    hardware_experience: 'none',
    robotics_experience: 'none',
    programming_languages: [],
    preferred_language: '',
    learning_goals: [],
    primary_interest: '',
    skill_level: 'student',
    education_level: '',
    industry: '',
    project_goals: '',
    time_commitment: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Available options for multi-select fields
  const programmingLanguageOptions = [
    'Python', 'C++', 'C', 'JavaScript', 'TypeScript', 'Java', 'Rust',
    'Go', 'MATLAB', 'R', 'Swift', 'Kotlin', 'Assembly', 'Other'
  ];

  const learningGoalOptions = [
    'Build robots from scratch',
    'AI and machine learning for robotics',
    'Computer vision and perception',
    'Motion planning and control',
    'ROS (Robot Operating System)',
    'Embedded systems programming',
    'Hardware design and electronics',
    'Research and academia',
    'Career transition to robotics',
    'Hobby projects'
  ];

  useEffect(() => {
    // Redirect if already completed
    if (user?.has_completed_questionnaire) {
      history.push('/dashboard');
    }
  }, [user, history]);

  const handleCheckboxChange = (field, value) => {
    setFormData(prev => {
      const currentValues = prev[field];
      if (currentValues.includes(value)) {
        return { ...prev, [field]: currentValues.filter(v => v !== value) };
      } else {
        return { ...prev, [field]: [...currentValues, value] };
      }
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Validation
    if (formData.programming_languages.length === 0) {
      setError('Please select at least one programming language');
      setLoading(false);
      return;
    }
    if (formData.learning_goals.length === 0) {
      setError('Please select at least one learning goal');
      setLoading(false);
      return;
    }

    // Convert years_coding to number
    const submitData = {
      ...formData,
      years_coding: formData.years_coding ? parseInt(formData.years_coding) : null
    };

    const result = await submitQuestionnaire(submitData);

    if (result.success) {
      history.push('/dashboard');
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  const formStyle = {
    maxWidth: '800px',
    margin: '2rem auto',
    padding: '2rem',
    background: 'rgba(0, 217, 255, 0.05)',
    border: '1px solid #00d9ff',
    borderRadius: '8px',
    boxShadow: '0 0 20px rgba(0, 217, 255, 0.2)'
  };

  const sectionStyle = {
    marginBottom: '2rem',
    paddingBottom: '2rem',
    borderBottom: '1px solid rgba(0, 217, 255, 0.2)'
  };

  const labelStyle = {
    display: 'block',
    color: '#00d9ff',
    marginBottom: '0.5rem',
    fontWeight: 'bold',
    textTransform: 'uppercase',
    fontSize: '0.9rem',
    letterSpacing: '1px'
  };

  const inputStyle = {
    width: '100%',
    padding: '0.75rem',
    background: 'rgba(0, 217, 255, 0.1)',
    border: '1px solid #00d9ff',
    borderRadius: '4px',
    color: '#e0e0e0',
    fontSize: '1rem',
    outline: 'none'
  };

  const checkboxContainerStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
    gap: '1rem',
    marginTop: '1rem'
  };

  const checkboxLabelStyle = {
    display: 'flex',
    alignItems: 'center',
    color: '#e0e0e0',
    cursor: 'pointer',
    padding: '0.5rem',
    borderRadius: '4px',
    transition: 'background 0.3s ease'
  };

  return (
    <Layout title="Background Questionnaire" description="Tell us about your experience">
      <div style={formStyle}>
        <h1 style={{
          color: '#00ffff',
          textAlign: 'center',
          marginBottom: '1rem',
          textTransform: 'uppercase',
          letterSpacing: '2px'
        }}>
          Background Questionnaire
        </h1>
        <p style={{ textAlign: 'center', color: '#888', marginBottom: '2rem' }}>
          Help us personalize your learning experience
        </p>

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
          {/* Section 1: Software Experience */}
          <div style={sectionStyle}>
            <h2 style={{ color: '#00d9ff', marginBottom: '1.5rem' }}>Software Experience</h2>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Software Experience Level</label>
              <select
                value={formData.software_experience}
                onChange={(e) => setFormData({ ...formData, software_experience: e.target.value })}
                required
                style={inputStyle}
              >
                <option value="beginner">Beginner - Just starting out</option>
                <option value="intermediate">Intermediate - Some experience</option>
                <option value="advanced">Advanced - Solid experience</option>
                <option value="expert">Expert - Professional level</option>
              </select>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Years of Coding Experience</label>
              <input
                type="number"
                min="0"
                max="50"
                value={formData.years_coding}
                onChange={(e) => setFormData({ ...formData, years_coding: e.target.value })}
                placeholder="Optional"
                style={inputStyle}
              />
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Programming Languages (Select all that apply)</label>
              <div style={checkboxContainerStyle}>
                {programmingLanguageOptions.map(lang => (
                  <label key={lang} style={checkboxLabelStyle}>
                    <input
                      type="checkbox"
                      checked={formData.programming_languages.includes(lang)}
                      onChange={() => handleCheckboxChange('programming_languages', lang)}
                      style={{ marginRight: '0.5rem', cursor: 'pointer' }}
                    />
                    {lang}
                  </label>
                ))}
              </div>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Preferred Programming Language</label>
              <input
                type="text"
                value={formData.preferred_language}
                onChange={(e) => setFormData({ ...formData, preferred_language: e.target.value })}
                required
                placeholder="e.g., Python, C++"
                style={inputStyle}
              />
            </div>
          </div>

          {/* Section 2: Hardware & Robotics */}
          <div style={sectionStyle}>
            <h2 style={{ color: '#00d9ff', marginBottom: '1.5rem' }}>Hardware & Robotics Experience</h2>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Hardware Experience</label>
              <select
                value={formData.hardware_experience}
                onChange={(e) => setFormData({ ...formData, hardware_experience: e.target.value })}
                required
                style={inputStyle}
              >
                <option value="none">None - No hardware experience</option>
                <option value="hobby">Hobby - Personal projects</option>
                <option value="professional">Professional - Work experience</option>
                <option value="expert">Expert - Deep expertise</option>
              </select>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Robotics Experience</label>
              <select
                value={formData.robotics_experience}
                onChange={(e) => setFormData({ ...formData, robotics_experience: e.target.value })}
                required
                style={inputStyle}
              >
                <option value="none">None - New to robotics</option>
                <option value="beginner">Beginner - Basic knowledge</option>
                <option value="intermediate">Intermediate - Some projects</option>
                <option value="advanced">Advanced - Extensive experience</option>
              </select>
            </div>
          </div>

          {/* Section 3: Learning Goals */}
          <div style={sectionStyle}>
            <h2 style={{ color: '#00d9ff', marginBottom: '1.5rem' }}>Learning Goals</h2>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>What are your learning goals? (Select all that apply)</label>
              <div style={checkboxContainerStyle}>
                {learningGoalOptions.map(goal => (
                  <label key={goal} style={checkboxLabelStyle}>
                    <input
                      type="checkbox"
                      checked={formData.learning_goals.includes(goal)}
                      onChange={() => handleCheckboxChange('learning_goals', goal)}
                      style={{ marginRight: '0.5rem', cursor: 'pointer' }}
                    />
                    {goal}
                  </label>
                ))}
              </div>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Primary Interest Area</label>
              <input
                type="text"
                value={formData.primary_interest}
                onChange={(e) => setFormData({ ...formData, primary_interest: e.target.value })}
                required
                placeholder="e.g., AI/Vision, Motion Control, Hardware Design"
                style={inputStyle}
              />
            </div>
          </div>

          {/* Section 4: Background */}
          <div style={sectionStyle}>
            <h2 style={{ color: '#00d9ff', marginBottom: '1.5rem' }}>Background Information</h2>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Current Skill Level</label>
              <select
                value={formData.skill_level}
                onChange={(e) => setFormData({ ...formData, skill_level: e.target.value })}
                required
                style={inputStyle}
              >
                <option value="student">Student</option>
                <option value="professional">Professional</option>
                <option value="researcher">Researcher</option>
                <option value="hobbyist">Hobbyist</option>
              </select>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Education Level</label>
              <select
                value={formData.education_level}
                onChange={(e) => setFormData({ ...formData, education_level: e.target.value })}
                required
                style={inputStyle}
              >
                <option value="">Select...</option>
                <option value="high_school">High School</option>
                <option value="bachelors">Bachelor's Degree</option>
                <option value="masters">Master's Degree</option>
                <option value="phd">PhD</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Industry (Optional)</label>
              <input
                type="text"
                value={formData.industry}
                onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                placeholder="e.g., Manufacturing, Healthcare, Aerospace"
                style={inputStyle}
              />
            </div>
          </div>

          {/* Section 5: Additional Information */}
          <div style={{ marginBottom: '2rem' }}>
            <h2 style={{ color: '#00d9ff', marginBottom: '1.5rem' }}>Additional Information</h2>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Project Goals (Optional)</label>
              <textarea
                value={formData.project_goals}
                onChange={(e) => setFormData({ ...formData, project_goals: e.target.value })}
                placeholder="Tell us about any specific projects or goals you have in mind..."
                rows="4"
                style={{ ...inputStyle, resize: 'vertical' }}
              />
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={labelStyle}>Time Commitment (Optional)</label>
              <select
                value={formData.time_commitment}
                onChange={(e) => setFormData({ ...formData, time_commitment: e.target.value })}
                style={inputStyle}
              >
                <option value="">Select...</option>
                <option value="1-5">1-5 hours/week</option>
                <option value="5-10">5-10 hours/week</option>
                <option value="10-20">10-20 hours/week</option>
                <option value="20+">20+ hours/week</option>
              </select>
            </div>
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
          >
            {loading ? 'Submitting...' : 'Complete Questionnaire'}
          </button>
        </form>
      </div>
    </Layout>
  );
}

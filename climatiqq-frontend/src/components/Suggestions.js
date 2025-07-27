import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Suggestions.css';

const Suggestions = ({ token, darkMode }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [dataPoints, setDataPoints] = useState(0);

  const getSuggestions = async () => {
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('https://green-track.onrender.com/api/v1/ai-suggestions/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        }
      });

      const data = await response.json();

      if (response.ok) {
        setSuggestions(data.suggestions || []);
        setDataPoints(data.data_points_analyzed || 0);
      } else {
        setError(data.error || 'Failed to get suggestions');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    getSuggestions();
  }, []);

  return (
    <div className={`suggestions ${darkMode ? 'dark' : ''}`}>
      <header className="suggestions-header">
        <Link to="/dashboard" className="back-link">← Back to Dashboard</Link>
        <h1>🤖 AI Climate Suggestions</h1>
      </header>

      <div className="suggestions-content">
        {isLoading ? (
          <div className="loading-suggestions">
            <div className="loading-spinner"></div>
            <p>Analyzing your carbon data and generating personalized suggestions...</p>
          </div>
        ) : error ? (
          <div className="error-suggestions">
            <p>{error}</p>
            <button onClick={getSuggestions} className="btn btn-primary">
              Try Again
            </button>
          </div>
        ) : (
          <>
            <div className="suggestions-grid">
              {suggestions.map((suggestion, index) => (
                <div key={index} className="suggestion-card">
                  <div className="suggestion-header">
                    <h3>{suggestion.title}</h3>
                    <div className="suggestion-meta">
                      <span className={`impact-badge impact-${suggestion.impact.toLowerCase()}`}>
                        {suggestion.impact} Impact
                      </span>
                      <span className={`effort-badge effort-${suggestion.effort.toLowerCase()}`}>
                        {suggestion.effort} Effort
                      </span>
                    </div>
                  </div>
                  
                  <div className="suggestion-content">
                    <p>{suggestion.message}</p>
                  </div>
                </div>
              ))}
              
              {dataPoints > 0 && (
                <div className="data-points-info">
                  <p>Based on {dataPoints} data points from your entries</p>
                </div>
              )}
            </div>

            <div className="suggestion-actions">
              <button onClick={getSuggestions} className="btn btn-secondary">
                Get New Suggestions
              </button>
              <Link to="/dashboard" className="btn btn-primary">
                Back to Dashboard
              </Link>
            </div>
          </>
        )}

        <div className="suggestions-info">
          <h3>How it works:</h3>
          <ul>
            <li>Our AI analyzes your carbon usage patterns</li>
            <li>Provides personalized, actionable advice</li>
            <li>Gets smarter as you add more data</li>
            <li>Focuses on practical, achievable changes</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Suggestions; 
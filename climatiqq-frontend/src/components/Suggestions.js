import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import apiService from '../services/api';
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
      // Use the apiService which now points to localhost:8000
      const data = await apiService.ai.getSuggestions({});

      if (data && data.suggestions) {
        setSuggestions(data.suggestions || []);
        setDataPoints(data.data_points_analyzed || 0);
      } else {
        setError('No suggestions received from AI');
      }
    } catch (err) {
      console.error('AI suggestions error:', err);
      setError(err.message || 'Failed to get suggestions. Please try again.');
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
      </div>
    </div>
  );
};

export default Suggestions; 
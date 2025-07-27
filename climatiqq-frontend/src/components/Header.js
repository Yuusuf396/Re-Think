import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = ({ onLogout, isAuthenticated, darkMode, onToggleDarkMode }) => {
  return (
    <header className={`header ${darkMode ? 'dark' : ''}`}>
      <div className="header-content">
        <Link to="/dashboard" className="logo">
          <div className="logo-icon">
            <div className="logo-r">
              <div className="r-stem"></div>
              <div className="r-loop"></div>
            </div>
            <div className="logo-leaves">
              <div className="leaf leaf-1"></div>
              <div className="leaf leaf-2"></div>
              <div className="leaf leaf-3"></div>
            </div>
          </div>
          <span className="logo-text">Rethink</span>
        </Link>
        
        {isAuthenticated && (
          <nav className="nav-menu">
            <Link to="/dashboard" className="nav-link">Dashboard</Link>
            <Link to="/suggestions" className="nav-link">AI Suggestions</Link>
            <Link to="/profile" className="nav-link">Profile</Link>
            <button onClick={onToggleDarkMode} className="dark-mode-toggle">
              {darkMode ? "☀️" : "🌙"}
            </button>
            <button onClick={onLogout} className="nav-link logout-btn">Logout</button>
          </nav>
        )}
      </div>
    </header>
  );
};

export default Header; 
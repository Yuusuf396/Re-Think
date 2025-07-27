import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import Suggestions from './components/Suggestions';
import Header from './components/Header';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';
import Profile from './components/Profile';
import apiService from './services/api';
import './App.css';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [token, setToken] = useState(null);
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [darkMode, setDarkMode] = useState(true);

    // Load dark mode preference from localStorage
    useEffect(() => {
        const savedDarkMode = localStorage.getItem('darkMode');
        if (savedDarkMode !== null) {
            setDarkMode(JSON.parse(savedDarkMode));
        }
    }, []);

    // Save dark mode preference to localStorage
    useEffect(() => {
        localStorage.setItem('darkMode', JSON.stringify(darkMode));
        // Apply dark mode to body
        if (darkMode) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    }, [darkMode]);

    // Check authentication status on app load
    useEffect(() => {
        const savedToken = localStorage.getItem('token');
        if (savedToken) {
            setToken(savedToken);
            setIsAuthenticated(true);
        }
        setIsLoading(false);
    }, []);

    const handleLogin = (newToken, userData) => {
        setToken(newToken);
        setUser(userData);
        setIsAuthenticated(true);
        localStorage.setItem('token', newToken);
    };

    const handleLogout = async () => {
        try {
            // Call enhanced logout API
            await apiService.auth.logout();
        } catch (error) {
            console.error('Logout error:', error);
            // Continue with logout even if API call fails
        } finally {
            // Clear local state
            setToken(null);
            setUser(null);
            setIsAuthenticated(false);
            localStorage.removeItem('token');
            localStorage.removeItem('refreshToken');
        }
    };

    const toggleDarkMode = () => {
        setDarkMode(!darkMode);
    };

    if (isLoading) {
        return (
            <div className={`App ${darkMode ? 'dark' : ''}`}>
                <div className="loading-spinner">
                    <div className="spinner"></div>
                    <p>Loading Rethink...</p>
                </div>
            </div>
        );
    }

    return (
        <div className={`App ${darkMode ? 'dark' : ''}`}>
            <Router>
                <Header 
                    onLogout={handleLogout} 
                    isAuthenticated={isAuthenticated}
                    darkMode={darkMode}
                    onToggleDarkMode={toggleDarkMode}
                />
                <Routes>
                    <Route 
                        path="/login" 
                        element={
                            isAuthenticated ? 
                            <Navigate to="/dashboard" /> : 
                            <Login onLogin={handleLogin} darkMode={darkMode} />
                        } 
                    />
                    <Route 
                        path="/register" 
                        element={
                            isAuthenticated ? 
                            <Navigate to="/dashboard" /> : 
                            <Register onLogin={handleLogin} darkMode={darkMode} />
                        } 
                    />
                    <Route 
                        path="/forgot-password" 
                        element={
                            isAuthenticated ? 
                            <Navigate to="/dashboard" /> : 
                            <ForgotPassword darkMode={darkMode} />
                        } 
                    />
                    <Route 
                        path="/reset-password/:token" 
                        element={
                            isAuthenticated ? 
                            <Navigate to="/dashboard" /> : 
                            <ResetPassword darkMode={darkMode} />
                        } 
                    />
                    <Route 
                        path="/dashboard" 
                        element={
                            isAuthenticated ? 
                            <Dashboard token={token} darkMode={darkMode} /> : 
                            <Navigate to="/login" />
                        } 
                    />
                    <Route 
                        path="/suggestions" 
                        element={
                            isAuthenticated ? 
                            <Suggestions token={token} darkMode={darkMode} /> : 
                            <Navigate to="/login" />
                        } 
                    />
                    <Route 
                        path="/profile" 
                        element={
                            isAuthenticated ? 
                            <Profile token={token} darkMode={darkMode} /> : 
                            <Navigate to="/login" />
                        } 
                    />
                    <Route 
                        path="/" 
                        element={
                            isAuthenticated ? 
                            <Navigate to="/dashboard" /> : 
                            <Navigate to="/login" />
                        } 
                    />
                </Routes>
            </Router>
        </div>
    );
}

export default App;

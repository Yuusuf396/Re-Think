import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import apiService from '../services/api';
import './Login.css';

const Login = ({ onLogin, darkMode }) => {
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
        setError(''); // Clear error when user types
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            // Use enhanced auth API
            const response = await apiService.auth.login({
                username: formData.username,
                password: formData.password,
                rememberMe: false
            });

            // Store tokens
            if (response && response.access) {
                localStorage.setItem('token', response.access);
                localStorage.setItem('refreshToken', response.refresh || '');
            }

            // Call parent login handler
            onLogin(response?.access || '', response?.user || {});

            // Navigate to dashboard
            navigate('/dashboard');

        } catch (error) {
            console.error('Login error:', error);
            setError(error.message || 'Login failed. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={`login-container ${darkMode ? 'dark' : ''}`}>
            <div className="login-card">
                <div className="logo-section">
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
                    <div className="logo-text">Rethink</div>
                </div>

                <h2>Welcome Back</h2>
                <p>Sign in to continue your sustainability journey</p>

                {/* Important Notice */}
                <div className="important-notice">
                    <div className="notice-icon">⚠️</div>
                    <div className="notice-content">
                        <strong>Important:</strong> Use your username (not email) to login
                    </div>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            type="text"
                            id="username"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            required
                            disabled={isLoading}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            disabled={isLoading}
                        />
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <button type="submit" disabled={isLoading}>
                        {isLoading ? 'Signing In...' : 'Sign In'}
                    </button>
                </form>

                <div className="login-links">
                    <Link to="/forgot-password" className="forgot-password-link">
                        Forgot Password?
                    </Link>
                    <p className="register-link">
                        Don't have an account? <Link to="/register">Sign Up</Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login; 
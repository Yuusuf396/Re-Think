import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import apiService from '../services/api';
import './Register.css';

const Register = ({ onLogin, darkMode }) => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        passwordConfirm: ''
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

        // Validate passwords match
        if (formData.password !== formData.passwordConfirm) {
            setError('Passwords do not match');
            setIsLoading(false);
            return;
        }

        try {
            // Use enhanced auth API
            const response = await apiService.auth.register({
                username: formData.username,
                email: formData.email,
                password: formData.password,
                passwordConfirm: formData.passwordConfirm
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
            console.error('Registration error:', error);
            setError(error.message || 'Registration failed. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={`register-container ${darkMode ? 'dark' : ''}`}>
            <div className="register-card">
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

                <h2>Create Account</h2>
                <p>Join us in tracking your environmental impact</p>

                {/* Important Notices */}
                <div className="important-notice">
                    <div className="notice-icon">⚠️</div>
                    <div className="notice-content">
                        <strong>Important:</strong> Remember your username and password - no password reset available yet
                    </div>
                </div>

                <div className="important-notice">
                    <div className="notice-icon">💡</div>
                    <div className="notice-content">
                        <strong>Tip:</strong> Use your username (not email) to login after registration
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
                            minLength="3"
                            maxLength="30"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
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
                            minLength="8"
                        />
                        <small>Password must be at least 8 characters with uppercase, lowercase, and numbers</small>
                    </div>

                    <div className="form-group">
                        <label htmlFor="passwordConfirm">Confirm Password</label>
                        <input
                            type="password"
                            id="passwordConfirm"
                            name="passwordConfirm"
                            value={formData.passwordConfirm}
                            onChange={handleChange}
                            required
                            disabled={isLoading}
                        />
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <button type="submit" disabled={isLoading}>
                        {isLoading ? 'Creating Account...' : 'Create Account'}
                    </button>
                </form>

                <div className="register-links">
                    <p className="login-link">
                        Already have an account? <Link to="/login">Sign In</Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Register; 
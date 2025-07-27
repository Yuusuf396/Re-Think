import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import apiService from '../services/api';
import './ForgotPassword.css';

const ForgotPassword = ({ darkMode }) => {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        setSuccess('');

        try {
            // Use enhanced auth API
            await apiService.auth.requestPasswordReset(email);
            
            setSuccess('If this email is registered, you will receive a password reset link.');
            setEmail(''); // Clear form on success
            
        } catch (error) {
            console.error('Password reset request error:', error);
            setError(error.message || 'Failed to send reset email. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={`forgot-password-container ${darkMode ? 'dark' : ''}`}>
            <div className="forgot-password-card">
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

                <h2>Reset Password</h2>
                <p>Enter your email address and we'll send you a link to reset your password.</p>

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="email">Email Address</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            disabled={isLoading}
                        />
                    </div>

                    {error && <div className="error-message">{error}</div>}
                    {success && <div className="success-message">{success}</div>}

                    <button type="submit" disabled={isLoading}>
                        {isLoading ? 'Sending...' : 'Send Reset Link'}
                    </button>
                </form>

                <div className="back-to-login">
                    <Link to="/login">← Back to Sign In</Link>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword; 
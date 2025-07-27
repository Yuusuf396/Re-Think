import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import apiService from '../services/api';
import './ResetPassword.css';

const ResetPassword = ({ darkMode }) => {
    const [formData, setFormData] = useState({
        newPassword: '',
        newPasswordConfirm: ''
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isValidToken, setIsValidToken] = useState(false);
    const { token } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        // Validate token on component mount
        if (token) {
            setIsValidToken(true);
        } else {
            setError('Invalid reset link. Please request a new password reset.');
        }
    }, [token]);

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
        if (formData.newPassword !== formData.newPasswordConfirm) {
            setError('Passwords do not match');
            setIsLoading(false);
            return;
        }

        // Validate password strength
        if (formData.newPassword.length < 8) {
            setError('Password must be at least 8 characters long');
            setIsLoading(false);
            return;
        }

        try {
            // Use enhanced auth API
            await apiService.auth.confirmPasswordReset(
                token,
                formData.newPassword,
                formData.newPasswordConfirm
            );
            
            setSuccess('Password reset successful! You can now login with your new password.');
            
            // Redirect to login after 2 seconds
            setTimeout(() => {
                navigate('/login');
            }, 2000);
            
        } catch (error) {
            console.error('Password reset error:', error);
            setError(error.message || 'Password reset failed. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    if (!isValidToken) {
        return (
            <div className={`reset-password-container ${darkMode ? 'dark' : ''}`}>
                <div className="reset-password-card">
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

                    <h2>Invalid Reset Link</h2>
                    <p>The password reset link is invalid or has expired.</p>
                    
                    {error && <div className="error-message">{error}</div>}

                    <div className="back-to-login">
                        <Link to="/login">← Back to Sign In</Link>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className={`reset-password-container ${darkMode ? 'dark' : ''}`}>
            <div className="reset-password-card">
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

                <h2>Set New Password</h2>
                <p>Enter your new password below.</p>

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="newPassword">New Password</label>
                        <input
                            type="password"
                            id="newPassword"
                            name="newPassword"
                            value={formData.newPassword}
                            onChange={handleChange}
                            required
                            disabled={isLoading}
                            minLength="8"
                        />
                        <small>Password must be at least 8 characters with uppercase, lowercase, and numbers</small>
                    </div>

                    <div className="form-group">
                        <label htmlFor="newPasswordConfirm">Confirm New Password</label>
                        <input
                            type="password"
                            id="newPasswordConfirm"
                            name="newPasswordConfirm"
                            value={formData.newPasswordConfirm}
                            onChange={handleChange}
                            required
                            disabled={isLoading}
                        />
                    </div>

                    {error && <div className="error-message">{error}</div>}
                    {success && <div className="success-message">{success}</div>}

                    <button type="submit" disabled={isLoading}>
                        {isLoading ? 'Resetting Password...' : 'Reset Password'}
                    </button>
                </form>

                <div className="back-to-login">
                    <Link to="/login">← Back to Sign In</Link>
                </div>
            </div>
        </div>
    );
};

export default ResetPassword; 
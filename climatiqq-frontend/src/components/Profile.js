import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import apiService from '../services/api';
import './Profile.css';

const Profile = ({ token, darkMode }) => {
  const [userData, setUserData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showChangePassword, setShowChangePassword] = useState(false);
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      setIsLoading(true);
      setError('');
      
      // Use the working legacy profile endpoint
      const data = await apiService.auth.getProfile();
      setUserData(data);
      
    } catch (err) {
      console.error('Profile fetch error:', err);
      setError('Failed to load user data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (passwordData.new_password !== passwordData.confirm_password) {
      setError('New passwords do not match');
      return;
    }

    // Use reduced password requirements for development
    if (passwordData.new_password.length < 3) {
      setError('Password must be at least 3 characters long');
      return;
    }

    try {
      // Use the working legacy change password endpoint
      await apiService.auth.changePassword({
        currentPassword: passwordData.current_password,
        newPassword: passwordData.new_password,
        newPasswordConfirm: passwordData.confirm_password
      });

      setSuccess('Password changed successfully! Check your email for a security notification.');
      setPasswordData({
        current_password: '',
        new_password: '',
        confirm_password: ''
      });
      setShowChangePassword(false);
      
    } catch (err) {
      console.error('Password change error:', err);
      setError(err.message || 'Failed to change password');
    }
  };

  const sendVerificationEmail = async () => {
    try {
      // Use the working legacy email verification endpoint
      await apiService.auth.sendEmailVerification();
      setSuccess('Verification email sent successfully!');
    } catch (err) {
      console.error('Email verification error:', err);
      setError(err.message || 'Failed to send verification email');
    }
  };

  if (isLoading) {
    return (
      <div className={`profile ${darkMode ? 'dark' : ''}`}>
        <div className="loading">Loading profile...</div>
      </div>
    );
  }

  return (
    <div className={`profile ${darkMode ? 'dark' : ''}`}>
      <header className="profile-header">
        <Link to="/dashboard" className="back-link">← Back to Dashboard</Link>
        <h1>👤 User Profile</h1>
      </header>

      {/* Important Notice */}
      <div className="important-notice">
        <div className="notice-icon">🔐</div>
        <div className="notice-content">
          <strong>Password Security:</strong> Remember your password - no password reset available yet. Keep it safe!
        </div>
      </div>

      <div className="profile-content">
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        {userData && (
          <div className="profile-section">
            <h2>Account Information</h2>
            <div className="profile-info">
              <div className="info-item">
                <label>Username:</label>
                <span>{userData.username}</span>
              </div>
              <div className="info-item">
                <label>Email:</label>
                <span>{userData.email}</span>
                {userData.email_verified === false && (
                  <button onClick={sendVerificationEmail} className="btn btn-secondary">
                    Verify Email
                  </button>
                )}
              </div>
              {userData.first_name && (
                <div className="info-item">
                  <label>First Name:</label>
                  <span>{userData.first_name}</span>
                </div>
              )}
              {userData.last_name && (
                <div className="info-item">
                  <label>Last Name:</label>
                  <span>{userData.last_name}</span>
                </div>
              )}
              <div className="info-item">
                <label>Date Joined:</label>
                <span>{new Date(userData.date_joined).toLocaleDateString()}</span>
              </div>
              {userData.last_login && (
                <div className="info-item">
                  <label>Last Login:</label>
                  <span>{new Date(userData.last_login).toLocaleDateString()}</span>
                </div>
              )}
              <div className="info-item">
                <label>Account Status:</label>
                <span className={userData.is_active ? 'status-active' : 'status-inactive'}>
                  {userData.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            </div>
          </div>
        )}

        <div className="profile-section">
          <h2>Security</h2>
          <button 
            onClick={() => setShowChangePassword(!showChangePassword)} 
            className="btn btn-primary"
          >
            Change Password
          </button>

          {showChangePassword && (
            <form onSubmit={handlePasswordChange} className="password-form">
              <div className="form-group">
                <label htmlFor="current-password">Current Password:</label>
                <input
                  type="password"
                  id="current-password"
                  value={passwordData.current_password}
                  onChange={(e) => setPasswordData({...passwordData, current_password: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="new-password">New Password:</label>
                <input
                  type="password"
                  id="new-password"
                  value={passwordData.new_password}
                  onChange={(e) => setPasswordData({...passwordData, new_password: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="confirm-password">Confirm New Password:</label>
                <input
                  type="password"
                  id="confirm-password"
                  value={passwordData.confirm_password}
                  onChange={(e) => setPasswordData({...passwordData, confirm_password: e.target.value})}
                  required
                />
              </div>
              <div className="form-actions">
                <button type="submit" className="btn btn-primary">Change Password</button>
                <button 
                  type="button" 
                  onClick={() => setShowChangePassword(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile; 
// API Service for Rethink - Centralized API calls
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://green-track.onrender.com/api/v1';

class ApiService {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    // Helper method to get auth headers
    getAuthHeaders() {
        const token = localStorage.getItem('token');
        return {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        };
    }

    // Generic request method
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: this.getAuthHeaders(),
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            // Check if response is JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error(`Expected JSON response but got ${contentType}. Server may be down or endpoint not found.`);
            }
            
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || data.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            return data;
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    }

    // Authentication API calls - USING WORKING LEGACY ENDPOINTS
    auth = {
        // Registration - using legacy endpoint
        register: async (userData) => {
            return this.request('/register/', {
                method: 'POST',
                body: JSON.stringify({
                    username: userData.username,
                    email: userData.email,
                    password: userData.password,
                    password_confirm: userData.passwordConfirm
                })
            });
        },

        // Login - using legacy endpoint
        login: async (credentials) => {
            return this.request('/login/', {
                method: 'POST',
                body: JSON.stringify({
                    username: credentials.username,
                    password: credentials.password
                })
            });
        },

        // Logout - using legacy endpoint
        logout: async () => {
            return this.request('/logout/', {
                method: 'POST'
            });
        },

        // Password change - using legacy endpoint
        changePassword: async (passwordData) => {
            return this.request('/change-password/', {
                method: 'POST',
                body: JSON.stringify({
                    current_password: passwordData.currentPassword,
                    new_password: passwordData.newPassword,
                    new_password_confirm: passwordData.newPasswordConfirm
                })
            });
        },

        // Password reset request - using legacy endpoint
        requestPasswordReset: async (email) => {
            return this.request('/password-reset/', {
                method: 'POST',
                body: JSON.stringify({ email })
            });
        },

        // Password reset confirmation - using legacy endpoint
        confirmPasswordReset: async (token, newPassword, newPasswordConfirm) => {
            return this.request('/password-reset/confirm/', {
                method: 'POST',
                body: JSON.stringify({
                    token,
                    new_password: newPassword,
                    new_password_confirm: newPasswordConfirm
                })
            });
        },

        // Get user profile - using legacy endpoint
        getProfile: async () => {
            return this.request('/profile/');
        },

        // Update user profile - using legacy endpoint
        updateProfile: async (profileData) => {
            return this.request('/profile/', {
                method: 'PUT',
                body: JSON.stringify(profileData)
            });
        },

        // Email verification - using legacy endpoint
        sendEmailVerification: async () => {
            return this.request('/email-verification/', {
                method: 'POST'
            });
        },

        // Email verification confirmation - using legacy endpoint
        confirmEmailVerification: async (token) => {
            return this.request('/email-verification/confirm/', {
                method: 'POST',
                body: JSON.stringify({ token })
            });
        }
    };

    // Impact entries API calls
    entries = {
        // Get all entries
        getAll: async () => {
            return this.request('/entries/');
        },

        // Create new entry
        create: async (entryData) => {
            return this.request('/entries/', {
                method: 'POST',
                body: JSON.stringify(entryData)
            });
        },

        // Get single entry
        getById: async (id) => {
            return this.request(`/entries/${id}/`);
        },

        // Update entry
        update: async (id, entryData) => {
            return this.request(`/entries/${id}/`, {
                method: 'PUT',
                body: JSON.stringify(entryData)
            });
        },

        // Delete entry
        delete: async (id) => {
            return this.request(`/entries/${id}/`, {
                method: 'DELETE'
            });
        }
    };

    // Statistics API calls
    stats = {
        // Get impact statistics
        getImpactStats: async () => {
            return this.request('/stats/');
        }
    };

    // AI suggestions API calls
    ai = {
        // Get AI suggestions
        getSuggestions: async (userData) => {
            return this.request('/ai-suggestions/', {
                method: 'POST',
                body: JSON.stringify(userData)
            });
        },

        // Get ChatGPT suggestions
        getChatGPTSuggestions: async (prompt) => {
            return this.request('/chatgpt-suggestions/', {
                method: 'POST',
                body: JSON.stringify({ prompt })
            });
        }
    };
}

// Create and export a single instance
const apiService = new ApiService();
export default apiService; 
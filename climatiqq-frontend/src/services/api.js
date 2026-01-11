// API Service for Rethink - Centralized API calls
const API_BASE_URL =
	process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1";

class ApiService {
	constructor() {
		this.baseURL = API_BASE_URL;
	}

	// Helper method to get auth headers
	getAuthHeaders() {
		const token = localStorage.getItem("token");
		return {
			"Content-Type": "application/json",
			...(token && { Authorization: `Bearer ${token}` }),
		};
	}

	// Generic request method
	async request(endpoint, options = {}) {
		const url = `${this.baseURL}${endpoint}`;
		const config = {
			headers: this.getAuthHeaders(),
			...options,
		};

		try {
			const response = await fetch(url, config);

			// Check if response is JSON
			const contentType = response.headers.get("content-type");
			if (!contentType || !contentType.includes("application/json")) {
				throw new Error(
					`Expected JSON response but got ${contentType}. Server may be down or endpoint not found.`
				);
			}

			const data = await response.json();

			if (!response.ok) {
				// Handle Django REST Framework validation errors
				let errorMessage = data.detail || data.error;

				// If no detail/error, check for field-specific errors
				if (!errorMessage) {
					const fieldErrors = [];
					for (const [field, messages] of Object.entries(data)) {
						if (Array.isArray(messages)) {
							fieldErrors.push(...messages);
						} else if (typeof messages === "string") {
							fieldErrors.push(messages);
						}
					}
					errorMessage =
						fieldErrors.length > 0
							? fieldErrors.join(". ")
							: `HTTP ${response.status}: ${response.statusText}`;
				}

				const error = new Error(errorMessage);
				error.response = data;
				throw error;
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
			return this.request("/register/", {
				method: "POST",
				body: JSON.stringify({
					username: userData.username,
					email: userData.email,
					password: userData.password,
					password_confirm: userData.passwordConfirm,
				}),
			});
		},

		// Login - using legacy endpoint
		login: async (credentials) => {
			return this.request("/login/", {
				method: "POST",
				body: JSON.stringify({
					username: credentials.username,
					password: credentials.password,
				}),
			});
		},

		// Logout - using legacy endpoint
		logout: async () => {
			return this.request("/logout/", {
				method: "POST",
			});
		},
	};

	// Impact entries API calls
	entries = {
		// Get all entries
		getAll: async (filters = {}) => {
			// Build query string from filters
			const params = new URLSearchParams();
			if (filters.metric_type && filters.metric_type !== "all") {
				params.append("metric_type", filters.metric_type);
			}

			const queryString = params.toString();
			const endpoint = queryString ? `/entries/?${queryString}` : "/entries/";
			return this.request(endpoint);
		},

		// Create new entry
		create: async (entryData) => {
			return this.request("/entries/", {
				method: "POST",
				body: JSON.stringify(entryData),
			});
		},

		// Get single entry
		getById: async (id) => {
			return this.request(`/entries/${id}/`);
		},

		// Update entry
		update: async (id, entryData) => {
			return this.request(`/entries/${id}/`, {
				method: "PUT",
				body: JSON.stringify(entryData),
			});
		},

		// Delete entry
		delete: async (id) => {
			return this.request(`/entries/${id}/`, {
				method: "DELETE",
			});
		},
	};

	// Statistics API calls
	stats = {
		// Get impact statistics
		getImpactStats: async () => {
			return this.request("/stats/");
		},
	};
}

// Create and export a single instance
const apiService = new ApiService();
export default apiService;

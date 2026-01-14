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

		// #region agent log
		fetch("http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				location: "api.js:20",
				message: "request method entry",
				data: {
					url,
					endpoint,
					hasMethod: !!options.method,
					hasBody: !!options.body,
					method: options.method,
					bodyPreview: options.body?.substring(0, 100),
					baseURL: this.baseURL,
				},
				timestamp: Date.now(),
				sessionId: "debug-session",
				runId: "run1",
				hypothesisId: "A",
			}),
		}).catch(() => {});
		// #endregion

		// #region agent log
		fetch("http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				location: "api.js:25",
				message: "Config built",
				data: {
					hasMethod: !!config.method,
					hasBody: !!config.body,
					method: config.method,
					bodyType: typeof config.body,
					headersKeys: Object.keys(config.headers || {}),
				},
				timestamp: Date.now(),
				sessionId: "debug-session",
				runId: "run1",
				hypothesisId: "A",
			}),
		}).catch(() => {});
		// #endregion

		try {
			// #region agent log
			fetch(
				"http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e",
				{
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						location: "api.js:30",
						message: "Before fetch call",
						data: { url, method: config.method, hasBody: !!config.body },
						timestamp: Date.now(),
						sessionId: "debug-session",
						runId: "run1",
						hypothesisId: "B",
					}),
				}
			).catch(() => {});
			// #endregion

			const response = await fetch(url, config);

			// #region agent log
			fetch(
				"http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e",
				{
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						location: "api.js:32",
						message: "After fetch call",
						data: {
							status: response.status,
							statusText: response.statusText,
							ok: response.ok,
							contentType: response.headers.get("content-type"),
							url: response.url,
						},
						timestamp: Date.now(),
						sessionId: "debug-session",
						runId: "run1",
						hypothesisId: "B",
					}),
				}
			).catch(() => {});
			// #endregion

			// Check if response is JSON
			const contentType = response.headers.get("content-type");
			if (!contentType || !contentType.includes("application/json")) {
				// #region agent log
				fetch(
					"http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e",
					{
						method: "POST",
						headers: { "Content-Type": "application/json" },
						body: JSON.stringify({
							location: "api.js:35",
							message: "Non-JSON response error",
							data: { contentType, status: response.status },
							timestamp: Date.now(),
							sessionId: "debug-session",
							runId: "run1",
							hypothesisId: "C",
						}),
					}
				).catch(() => {});
				// #endregion

				throw new Error(
					`Expected JSON response but got ${contentType}. Server may be down or endpoint not found.`
				);
			}

			const data = await response.json();

			// #region agent log
			fetch(
				"http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e",
				{
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						location: "api.js:41",
						message: "Response parsed",
						data: {
							ok: response.ok,
							status: response.status,
							hasData: !!data,
							hasAccess: !!data.access,
							hasUser: !!data.user,
							dataKeys: Object.keys(data || {}),
						},
						timestamp: Date.now(),
						sessionId: "debug-session",
						runId: "run1",
						hypothesisId: "C",
					}),
				}
			).catch(() => {});
			// #endregion

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

				// #region agent log
				fetch(
					"http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e",
					{
						method: "POST",
						headers: { "Content-Type": "application/json" },
						body: JSON.stringify({
							location: "api.js:58",
							message: "Response not ok, throwing error",
							data: { status: response.status, errorMessage, data },
							timestamp: Date.now(),
							sessionId: "debug-session",
							runId: "run1",
							hypothesisId: "D",
						}),
					}
				).catch(() => {});
				// #endregion

				const error = new Error(errorMessage);
				error.response = data;
				throw error;
			}

			// #region agent log
			fetch(
				"http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e",
				{
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						location: "api.js:65",
						message: "Request successful, returning data",
						data: { hasAccess: !!data.access, hasUser: !!data.user },
						timestamp: Date.now(),
						sessionId: "debug-session",
						runId: "run1",
						hypothesisId: "E",
					}),
				}
			).catch(() => {});
			// #endregion

			return data;
		} catch (error) {
			// #region agent log
			fetch(
				"http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e",
				{
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						location: "api.js:67",
						message: "Request error caught",
						data: {
							errorMessage: error.message,
							errorName: error.name,
							errorStack: error.stack?.substring(0, 200),
						},
						timestamp: Date.now(),
						sessionId: "debug-session",
						runId: "run1",
						hypothesisId: "D",
					}),
				}
			).catch(() => {});
			// #endregion

			console.error(`API Error (${endpoint}):`, error);
			throw error;
		}
	}

	// Authentication API calls - USING WORKING LEGACY ENDPOINTS
	auth = {
		// Registration - using legacy endpoint
		register: async (userData) => {
			// #region agent log
			fetch(
				"http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e",
				{
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						location: "api.js:75",
						message: "register method entry",
						data: {
							username: userData.username,
							email: userData.email,
							hasPassword: !!userData.password,
							hasPasswordConfirm: !!userData.passwordConfirm,
						},
						timestamp: Date.now(),
						sessionId: "debug-session",
						runId: "run1",
						hypothesisId: "A",
					}),
				}
			).catch(() => {});
			// #endregion

			const requestBody = {
				username: userData.username,
				email: userData.email,
				password: userData.password,
				password_confirm: userData.passwordConfirm,
			};

			// #region agent log
			fetch(
				"http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e",
				{
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						location: "api.js:82",
						message: "Before request call",
						data: { requestBody, bodyStringified: JSON.stringify(requestBody) },
						timestamp: Date.now(),
						sessionId: "debug-session",
						runId: "run1",
						hypothesisId: "A",
					}),
				}
			).catch(() => {});
			// #endregion

			return this.request("/register/", {
				method: "POST",
				body: JSON.stringify(requestBody),
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

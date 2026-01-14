import React, { useState, useEffect } from "react";
import {
	BrowserRouter as Router,
	Routes,
	Route,
	Navigate,
} from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Dashboard from "./components/Dashboard";
import apiService from "./services/api";
import "./App.css";

function App() {
	const [isAuthenticated, setIsAuthenticated] = useState(false);
	const [token, setToken] = useState(null);
	const [user, setUser] = useState(null);
	const [isLoading, setIsLoading] = useState(true);

	// Check authentication status on app load
	useEffect(() => {
		const savedToken = localStorage.getItem("token");
		const savedUserRaw = localStorage.getItem("user");
		if (savedToken) {
			setToken(savedToken);
			setIsAuthenticated(true);
		}
		if (savedUserRaw) {
			try {
				setUser(JSON.parse(savedUserRaw));
			} catch (err) {
				console.warn("Failed to parse saved user", err);
			}
		}
		setIsLoading(false);
	}, []);

	const handleLogin = (newToken, userData) => {
		// #region agent log
		fetch("http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				location: "App.js:38",
				message: "handleLogin called",
				data: {
					hasToken: !!newToken,
					hasUserData: !!userData,
					userDataKeys: userData ? Object.keys(userData) : [],
				},
				timestamp: Date.now(),
				sessionId: "debug-session",
				runId: "run1",
				hypothesisId: "F",
			}),
		}).catch(() => {});
		// #endregion

		setToken(newToken);
		setUser(userData);
		setIsAuthenticated(true);
		localStorage.setItem("token", newToken);
		localStorage.setItem("user", JSON.stringify(userData || {}));

		// #region agent log
		fetch("http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				location: "App.js:50",
				message: "handleLogin completed",
				data: {
					tokenInStorage: !!localStorage.getItem("token"),
					userInStorage: !!localStorage.getItem("user"),
				},
				timestamp: Date.now(),
				sessionId: "debug-session",
				runId: "run1",
				hypothesisId: "F",
			}),
		}).catch(() => {});
		// #endregion
	};

	const handleLogout = async () => {
		try {
			await apiService.auth.logout();
		} catch (error) {
			console.error("Logout error:", error);
		} finally {
			setToken(null);
			setUser(null);
			setIsAuthenticated(false);
			localStorage.removeItem("token");
			localStorage.removeItem("refreshToken");
			localStorage.removeItem("user");
		}
	};

	if (isLoading) {
		return (
			<div className="App">
				<div className="loading-spinner">
					<div className="spinner"></div>
					<p>Loading Rethink...</p>
				</div>
			</div>
		);
	}

	return (
		<div className="App">
			<Router>
				<Routes>
					<Route
						path="/login"
						element={
							isAuthenticated ? (
								<Navigate to="/dashboard" />
							) : (
								<Login onLogin={handleLogin} />
							)
						}
					/>
					<Route
						path="/register"
						element={
							isAuthenticated ? (
								<Navigate to="/dashboard" />
							) : (
								<Register onLogin={handleLogin} />
							)
						}
					/>
					<Route
						path="/dashboard"
						element={
							(() => {
								// #region agent log
								fetch("http://127.0.0.1:7242/ingest/22113505-b882-4f19-9832-adabec7f412e", {
									method: "POST",
									headers: { "Content-Type": "application/json" },
									body: JSON.stringify({
										location: "App.js:98",
										message: "Dashboard route check",
										data: {
											isAuthenticated,
											hasToken: !!token,
											hasUser: !!user,
										},
										timestamp: Date.now(),
										sessionId: "debug-session",
										runId: "run1",
										hypothesisId: "F",
									}),
								}).catch(() => {});
								// #endregion

								return isAuthenticated ? (
									<Dashboard
										token={token}
										user={user}
										onLogout={handleLogout}
									/>
								) : (
									<Navigate to="/login" />
								);
							})()
						}
					/>
					<Route
						path="/"
						element={
							isAuthenticated ? (
								<Navigate to="/dashboard" />
							) : (
								<Navigate to="/login" />
							)
						}
					/>
				</Routes>
			</Router>
		</div>
	);
}

export default App;

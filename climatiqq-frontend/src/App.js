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
		setToken(newToken);
		setUser(userData);
		setIsAuthenticated(true);
		localStorage.setItem("token", newToken);
		localStorage.setItem("user", JSON.stringify(userData || {}));
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
							isAuthenticated ? (
								<Dashboard
									token={token}
									user={user}
									onLogout={handleLogout}
								/>
							) : (
								<Navigate to="/login" />
							)
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

import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import apiService from "../services/api";
import "./Login.css";

const Login = ({ onLogin }) => {
	const [formData, setFormData] = useState({
		username: "",
		password: "",
		rememberMe: true,
	});
	const [showPassword, setShowPassword] = useState(false);
	const [error, setError] = useState("");
	const [isLoading, setIsLoading] = useState(false);
	const navigate = useNavigate();

	const handleChange = (e) => {
		const { name, value, type, checked } = e.target;
		setFormData((prev) => ({
			...prev,
			[name]: type === "checkbox" ? checked : value,
		}));
		setError("");
	};

	const handleSubmit = async (e) => {
		e.preventDefault();
		setIsLoading(true);
		setError("");

		try {
			const response = await apiService.auth.login({
				username: formData.username,
				password: formData.password,
				rememberMe: formData.rememberMe,
			});

			if (response && response.access) {
				localStorage.setItem("token", response.access);
				localStorage.setItem("refreshToken", response.refresh || "");
			}

			onLogin(response?.access || "", response?.user || {});
			navigate("/dashboard");
		} catch (error) {
			console.error("Login error:", error);
			setError(error.message || "Login failed. Please try again.");
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<div className="auth-page login-page">
			<div className="auth-shell">
				<div className="brand-panel">
					<div className="brand-top">
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
						<div className="brand-name">Rethink</div>
					</div>

					<h1>Track your impact, stay in control</h1>
					<p className="brand-copy">
						A clean, dashboard-inspired sign-in. Keep your carbon, water, and
						energy progress in one secure place.
					</p>

					<div className="kpi-grid">
						<div className="kpi-card">
							<div className="kpi-label">Carbon</div>
							<div className="kpi-value">-32%</div>
							<div className="kpi-chip positive">vs. last month</div>
						</div>
						<div className="kpi-card">
							<div className="kpi-label">Energy</div>
							<div className="kpi-value">+12%</div>
							<div className="kpi-chip neutral">trend watch</div>
						</div>
						<div className="kpi-card">
							<div className="kpi-label">Water</div>
							<div className="kpi-value">-18%</div>
							<div className="kpi-chip positive">optimized</div>
						</div>
					</div>

					<div className="brand-footer">
						<div className="foot-pill">Secure access</div>
						<span>Designed to mirror your dashboard experience.</span>
					</div>
				</div>

				<div className="form-panel">
					<div className="form-card">
						<div className="form-header">
							<div className="pill">Welcome back</div>
							<h2>Sign in to Rethink</h2>
							<p className="subtitle">
								Use your username (not email) to log in and pick up where you
								left off.
							</p>
						</div>

						<div className="notice subtle">
							{/* <span className="notice-icon"><AlertCircleIcon size={18} /></span> */}
							<span>Use your username (not email) to login.</span>
						</div>

						{error && <div className="error-banner">{error}</div>}

						<form onSubmit={handleSubmit} className="auth-form">
							<div className="form-group">
								<label htmlFor="username">
									Username <span className="label-hint">Required</span>
								</label>
								<div className="input-wrapper">
									<input
										type="text"
										id="username"
										name="username"
										value={formData.username}
										onChange={handleChange}
										required
										disabled={isLoading}
										placeholder="e.g. rethink_user"
									/>
								</div>
							</div>

							<div className="form-group">
								<label htmlFor="password">
									Password <span className="label-hint">Keep it safe</span>
								</label>
								<div className="input-wrapper with-action">
									<input
										type={showPassword ? "text" : "password"}
										id="password"
										name="password"
										value={formData.password}
										onChange={handleChange}
										required
										disabled={isLoading}
										placeholder="••••••••"
									/>
									<button
										type="button"
										className="input-action"
										onClick={() => setShowPassword((prev) => !prev)}
										disabled={isLoading}
									>
										{showPassword ? "Hide" : "Show"}
									</button>
								</div>
							</div>

							<div className="form-row">
								<label className="checkbox">
									<input
										type="checkbox"
										name="rememberMe"
										checked={formData.rememberMe}
										onChange={handleChange}
										disabled={isLoading}
									/>
									<span>Remember me</span>
								</label>
								<span className="muted-hint">Password reset coming soon</span>
							</div>

							<button type="submit" className="cta-button" disabled={isLoading}>
								{isLoading ? "Signing In..." : "Sign In"}
							</button>
						</form>

						<div className="switch-auth">
							<span>New here?</span>
							<Link to="/register">Create an account</Link>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Login;
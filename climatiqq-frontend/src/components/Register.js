import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import apiService from "../services/api";
import "./Register.css";

const Register = ({ onLogin }) => {
	const [formData, setFormData] = useState({
		username: "",
		email: "",
		password: "",
		passwordConfirm: "",
	});
	const [showPassword, setShowPassword] = useState(false);
	const [showPasswordConfirm, setShowPasswordConfirm] = useState(false);
	const [error, setError] = useState("");
	const [isLoading, setIsLoading] = useState(false);
	const navigate = useNavigate();

	const handleChange = (e) => {
		const { name, value } = e.target;
		setFormData((prev) => ({
			...prev,
			[name]: value,
		}));
		setError("");
	};

	const handleSubmit = async (e) => {
		e.preventDefault();
		setIsLoading(true);
		setError("");

		if (formData.password !== formData.passwordConfirm) {
			setError("Passwords do not match");
			setIsLoading(false);
			return;
		}

		try {
			const response = await apiService.auth.register({
				username: formData.username,
				email: formData.email,
				password: formData.password,
				passwordConfirm: formData.passwordConfirm,
			});

			if (response && response.access) {
				localStorage.setItem("token", response.access);
				localStorage.setItem("refreshToken", response.refresh || "");
			}

			onLogin(response?.access || "", response?.user || {});
			navigate("/dashboard");
		} catch (error) {
			console.error("Registration error:", error);
			setError(error.message || "Registration failed. Please try again.");
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<div className="auth-page register-page">
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

					<h1>Create your account, see your impact</h1>
					<p className="brand-copy">
						Join the dashboard experience that keeps carbon, water, and energy
						metrics front and center.
					</p>

					<div className="kpi-grid">
						<div className="kpi-card">
							<div className="kpi-label">Carbon</div>
							<div className="kpi-value">Goal: 1000 kg</div>
							<div className="kpi-chip positive">Progressive</div>
						</div>
						<div className="kpi-card">
							<div className="kpi-label">Energy</div>
							<div className="kpi-value">Smart alerts</div>
							<div className="kpi-chip neutral">Adaptive</div>
						</div>
						<div className="kpi-card">
							<div className="kpi-label">Water</div>
							<div className="kpi-value">Usage insights</div>
							<div className="kpi-chip positive">On track</div>
						</div>
					</div>

					<div className="brand-footer">
						<div className="foot-pill">Frictionless onboarding</div>
						<span>Styled to match the live dashboard visuals.</span>
					</div>
				</div>

				<div className="form-panel">
					<div className="form-card">
						<div className="form-header">
							<div className="pill">Start tracking</div>
							<h2>Create your Rethink account</h2>
							<p className="subtitle">
								Use a username you’ll remember—login uses username, not email.
							</p>
						</div>

						<div className="notice subtle">
							{/* <span className="notice-icon">⚠️</span> */}
							<span>
								No password reset yet. Store your username and password safely.
							</span>
						</div>
						<div className="notice tip">
							{/* <span className="notice-icon">💡</span> */}
							<span>Login after signup with your username (not email).</span>
						</div>

						{error && <div className="error-banner">{error}</div>}

						<form onSubmit={handleSubmit} className="auth-form">
							<div className="form-group">
								<label htmlFor="username">
									Username <span className="label-hint">3-30 characters</span>
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
										minLength="3"
										maxLength="30"
										placeholder="e.g. rethink_creator"
									/>
								</div>
							</div>

							<div className="form-group">
								<label htmlFor="email">
									Email <span className="label-hint">For notifications</span>
								</label>
								<div className="input-wrapper">
									<input
										type="email"
										id="email"
										name="email"
										value={formData.email}
										onChange={handleChange}
										required
										disabled={isLoading}
										placeholder="you@example.com"
									/>
								</div>
							</div>

							<div className="form-group">
								<label htmlFor="password">
									Password <span className="label-hint">Min 8 chars</span>
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
										minLength="8"
										placeholder="Secure password"
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
								<small className="input-hint">
									Use upper/lowercase, numbers for better strength.
								</small>
							</div>

							<div className="form-group">
								<label htmlFor="passwordConfirm">Confirm password</label>
								<div className="input-wrapper with-action">
									<input
										type={showPasswordConfirm ? "text" : "password"}
										id="passwordConfirm"
										name="passwordConfirm"
										value={formData.passwordConfirm}
										onChange={handleChange}
										required
										disabled={isLoading}
										placeholder="Repeat password"
									/>
									<button
										type="button"
										className="input-action"
										onClick={() => setShowPasswordConfirm((prev) => !prev)}
										disabled={isLoading}
									>
										{showPasswordConfirm ? "Hide" : "Show"}
									</button>
								</div>
							</div>

							<button
								type="submit"
								className="cta-button"
								disabled={isLoading}
							>
								{isLoading ? "Creating Account..." : "Create Account"}
							</button>
						</form>

						<div className="switch-auth">
							<span>Already have an account?</span>
							<Link to="/login">Sign in</Link>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Register;
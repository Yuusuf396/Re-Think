import React, { useState, useEffect, useCallback } from "react";
import {
	RadialBarChart,
	RadialBar,
	PolarGrid,
	PolarAngleAxis,
	ResponsiveContainer,
	Tooltip,
	LineChart,
	Line,
	XAxis,
	YAxis,
	CartesianGrid,
	Legend,
	Treemap,
	BarChart,
	Bar,
} from "recharts";
import {
	Activity,
	Droplets,
	Zap,
	Wind,
	Leaf,
	Database,
	Settings,
	HelpCircle,
	Home,
	LogOut,
	Moon,
	Sun,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import apiService from "../services/api";
import "./Dashboard.css";

const Dashboard = ({ token, user, onLogout }) => {
	const navigate = useNavigate();
	const [entries, setEntries] = useState([]);
	const [stats, setStats] = useState({});
	const [loading, setLoading] = useState(true);
	const [filtering, setFiltering] = useState(false);
	const [error, setError] = useState("");
	const [showAddModal, setShowAddModal] = useState(false);
	const [showDetailModal, setShowDetailModal] = useState(false);
	const [selectedEntry, setSelectedEntry] = useState(null);
	const [filterMetric, setFilterMetric] = useState("all");
	const [darkMode, setDarkMode] = useState(() => {
		const saved = localStorage.getItem("darkMode");
		return saved ? JSON.parse(saved) : false;
	});
	const [newEntry, setNewEntry] = useState({
		metric_type: "carbon",
		value: "",
		description: "",
	});

	// Save dark mode preference and apply to document
	useEffect(() => {
		localStorage.setItem("darkMode", JSON.stringify(darkMode));
		if (darkMode) {
			document.documentElement.classList.add("dark");
		} else {
			document.documentElement.classList.remove("dark");
		}
	}, [darkMode]);

	const toggleDarkMode = () => {
		setDarkMode(!darkMode);
	};

	const fetchData = useCallback(
		async (isFilterChange = false) => {
			try {
				if (isFilterChange) {
					setFiltering(true);
				} else {
					setLoading(true);
				}

				// Fetch entries and stats in parallel
				const [entriesResponse, statsResponse] = await Promise.all([
					apiService.entries.getAll({ metric_type: filterMetric }),
					apiService.stats.getImpactStats(),
				]);

				setEntries(entriesResponse);
				setStats(statsResponse);
				setError("");
			} catch (error) {
				console.error("Dashboard fetch error:", error);
				setError("Failed to load dashboard data. Please try again.");
			} finally {
				setLoading(false);
				setFiltering(false);
			}
		},
		[filterMetric]
	);

	// Initial load when token changes
	useEffect(() => {
		fetchData(false);
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [token]);

	// Filter changes - only fetch if we already have data
	useEffect(() => {
		if (entries.length > 0) {
			fetchData(true);
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [filterMetric]);

	const handleAddEntry = async (e) => {
		e.preventDefault();

		try {
			const response = await apiService.entries.create(newEntry);
			setEntries([response, ...entries]);
			setShowAddModal(false);
			setNewEntry({ metric_type: "carbon", value: "", description: "" });

			// Refresh stats
			const updatedStats = await apiService.stats.getImpactStats();
			setStats(updatedStats);
		} catch (error) {
			console.error("Add entry error:", error);
			setError("Failed to add entry. Please try again.");
		}
	};

	const handleDeleteEntry = async (id) => {
		if (window.confirm("Are you sure you want to delete this entry?")) {
			try {
				await apiService.entries.delete(id);
				setEntries(entries.filter((entry) => entry.id !== id));

				// Refresh stats
				const updatedStats = await apiService.stats.getImpactStats();
				setStats(updatedStats);
			} catch (error) {
				console.error("Delete entry error:", error);
				setError("Failed to delete entry. Please try again.");
			}
		}
	};

	const handleEntryClick = (entry) => {
		setSelectedEntry(entry);
		setShowDetailModal(true);
	};

	const getMetricIcon = (metricType) => {
		const icons = {
			carbon: <Leaf size={20} />,
			water: <Droplets size={20} />,
			energy: <Zap size={20} />,
			digital: <Database size={20} />,
		};
		return icons[metricType] || <Activity size={20} />;
	};

	const getMetricColor = (metricType) => {
		const colors = {
			carbon: "#10b981",
			water: "#3b82f6",
			energy: "#f59e0b",
			digital: "#8b5cf6",
		};
		return colors[metricType] || "#6b7280";
	};

	// Get metric by type from stats
	const getMetric = (type) => {
		return (
			stats?.metric_breakdown?.find((m) => m.metric_type === type) || {
				total_value: 0,
				avg_value: 0,
				count: 0,
			}
		);
	};

	const carbonData = getMetric("carbon");
	const waterData = getMetric("water");
	const energyData = getMetric("energy");
	const digitalData = getMetric("digital");
	const displayName = (user && (user.username || user.email)) || "there";

	// Radial chart data for carbon (progress ring showing % of 1000 kg goal)
	const carbonGoal = 1000;
	const carbonProgress = Math.min(
		(carbonData.total_value / carbonGoal) * 100,
		100
	);

	const radialData = [
		{
			name: "Carbon",
			value: carbonProgress,
			fill: "#10b981",
		},
	];

	// Treemap data for water usage breakdown
	const treemapData = [
		{
			name: "Water Usage",
			children: [
				{
					name: "Total Used",
					size: waterData.total_value || 1,
					fill: "#06b6d4",
				},
				{
					name: "Remaining",
					size: Math.max(500 - (waterData.total_value || 0), 1),
					fill: "#e0f2fe",
				},
			],
		},
	];

	// Activity data from entries (last 7 days)
	const getActivityData = () => {
		const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
		const activityMap = {};
		days.forEach((day) => (activityMap[day] = 0));

		entries.forEach((entry) => {
			const date = new Date(entry.created_at);
			const dayName = days[date.getDay()];
			activityMap[dayName] = (activityMap[dayName] || 0) + 1;
		});

		return days.map((day) => ({
			day,
			entries: activityMap[day] || 0,
		}));
	};

	const activityData = getActivityData();

	// Performance over time data (stacked bar chart)
	const getPerformanceData = () => {
		const monthMap = {};

		entries.forEach((entry) => {
			const date = new Date(entry.created_at);
			const monthKey = date.toLocaleDateString("en-US", { month: "short" });

			if (!monthMap[monthKey]) {
				monthMap[monthKey] = {
					month: monthKey,
					Carbon: 0,
					Water: 0,
					Energy: 0,
					Digital: 0,
				};
			}

			const metricKey =
				entry.metric_type.charAt(0).toUpperCase() + entry.metric_type.slice(1);
			monthMap[monthKey][metricKey] += parseFloat(entry.value) || 0;
		});

		return Object.values(monthMap);
	};

	const performanceData = getPerformanceData();

	// Custom tooltip for charts
	const CustomTooltip = ({ active, payload, label }) => {
		if (active && payload && payload.length) {
			return (
				<div className="vendico-tooltip">
					<p className="tooltip-label">{label}</p>
					{payload.map((entry, index) => (
						<p
							key={index}
							className="tooltip-item"
							style={{ color: entry.color }}>
							{entry.name}:{" "}
							{typeof entry.value === "number"
								? entry.value.toFixed(2)
								: entry.value}
						</p>
					))}
				</div>
			);
		}
		return null;
	};

	if (loading) {
		return (
			<div className={`vendico-dashboard ${darkMode ? "dark" : ""}`}>
				<div className="vendico-sidebar">
					<div className="sidebar-logo">
						<Leaf className="logo-icon" />
						<span>Rethink</span>
					</div>
				</div>
				<div className="vendico-main">
					<div className="loading-state">
						<div className="spinner"></div>
						<p>Loading dashboard...</p>
					</div>
				</div>
			</div>
		);
	}

	return (
		<div className={`vendico-dashboard ${darkMode ? "dark" : ""}`}>
			{/* Sidebar */}
			<div className="vendico-sidebar">
				<div className="sidebar-logo">
					<Leaf className="logo-icon" />
					<span>Rethink</span>
				</div>

				<nav className="sidebar-nav">
					<div className="nav-section">
						<span className="nav-section-title">MAIN</span>
						<button
							className="nav-item active"
							onClick={() => navigate("/dashboard")}>
							<Home size={18} />
							<span>Home</span>
						</button>
						<button className="nav-item">
							<Leaf size={18} />
							<span>Environment</span>
						</button>
					</div>

					<div className="nav-section">
						<span className="nav-section-title">OTHER</span>
						<button
							className="nav-item"
							onClick={toggleDarkMode}
							title={darkMode ? "Switch to light mode" : "Switch to dark mode"}>
							{darkMode ? <Sun size={18} /> : <Moon size={18} />}
							<span>{darkMode ? "Light Mode" : "Dark Mode"}</span>
						</button>
						<button className="nav-item">
							<Settings size={18} />
							<span>Settings</span>
						</button>
						<button className="nav-item">
							<HelpCircle size={18} />
							<span>Help</span>
						</button>
						<button
							className="nav-item"
							onClick={onLogout}>
							<LogOut size={18} />
							<span>Logout</span>
						</button>
					</div>
				</nav>
			</div>

			{/* Main Content */}
			<div className="vendico-main">
				{/* Top Bar */}
				<div className="vendico-topbar">
					<div className="topbar-left">
						<h1 className="page-title">Home</h1>
						<p className="welcome-text">Welcome back, {displayName}.</p>
					</div>
					<div className="topbar-right">
						<select className="topbar-select">
							<option>Last 7 days</option>
							<option>Last 30 days</option>
							<option>Last 90 days</option>
						</select>
						<button className="btn-view-insight">View Insight</button>
					</div>
				</div>

				{error && (
					<div className="error-banner">
						<span>{error}</span>
						<button onClick={() => setError("")}>×</button>
					</div>
				)}

				{/* Stats Cards */}
				<div className="stats-grid">
					<div className="stat-card">
						<div className="stat-card-header">
							<div
								className="stat-icon"
								style={{ background: "#e8f5e9" }}>
								<Leaf
									size={24}
									style={{ color: "#10b981" }}
								/>
							</div>
							<div className="stat-progress">
								<div className="progress-ring">
									<svg
										width="60"
										height="60">
										<circle
											cx="30"
											cy="30"
											r="26"
											fill="none"
											stroke="#e0e0e0"
											strokeWidth="4"
										/>
										<circle
											cx="30"
											cy="30"
											r="26"
											fill="none"
											stroke="#10b981"
											strokeWidth="4"
											strokeDasharray={`${(carbonData.total_value / 1000) * 163} 163`}
											transform="rotate(-90 30 30)"
										/>
									</svg>
									<span className="progress-text">
										{Math.min(
											(carbonData.total_value / 1000) * 100,
											100
										).toFixed(0)}
										%
									</span>
								</div>
							</div>
						</div>
						<div className="stat-card-body">
							<div className="stat-label">Carbon Footprint</div>
							<div className="stat-value">
								{carbonData.total_value.toFixed(1)} kg CO₂
							</div>
							<div className="stat-meta">Now: {carbonData.count} entries</div>
						</div>
					</div>

					<div className="stat-card">
						<div className="stat-card-header">
							<div
								className="stat-icon"
								style={{ background: "#e3f2fd" }}>
								<Droplets
									size={24}
									style={{ color: "#3b82f6" }}
								/>
							</div>
							<div className="stat-progress">
								<div className="progress-ring">
									<svg
										width="60"
										height="60">
										<circle
											cx="30"
											cy="30"
											r="26"
											fill="none"
											stroke="#e0e0e0"
											strokeWidth="4"
										/>
										<circle
											cx="30"
											cy="30"
											r="26"
											fill="none"
											stroke="#3b82f6"
											strokeWidth="4"
											strokeDasharray={`${(waterData.total_value / 500) * 163} 163`}
											transform="rotate(-90 30 30)"
										/>
									</svg>
									<span className="progress-text">
										{Math.min((waterData.total_value / 500) * 100, 100).toFixed(
											0
										)}
										%
									</span>
								</div>
							</div>
						</div>
						<div className="stat-card-body">
							<div className="stat-label">Water</div>
							<div className="stat-value">
								{waterData.total_value.toFixed(1)} L
							</div>
							<div className="stat-meta">Now: {waterData.count} entries</div>
						</div>
					</div>

					<div className="stat-card">
						<div className="stat-card-header">
							<div
								className="stat-icon"
								style={{ background: "#fff3e0" }}>
								<Zap
									size={24}
									style={{ color: "#f59e0b" }}
								/>
							</div>
							<div className="stat-progress">
								<div className="progress-ring">
									<svg
										width="60"
										height="60">
										<circle
											cx="30"
											cy="30"
											r="26"
											fill="none"
											stroke="#e0e0e0"
											strokeWidth="4"
										/>
										<circle
											cx="30"
											cy="30"
											r="26"
											fill="none"
											stroke="#f59e0b"
											strokeWidth="4"
											strokeDasharray={`${(energyData.total_value / 200) * 163} 163`}
											transform="rotate(-90 30 30)"
										/>
									</svg>
									<span className="progress-text">
										{Math.min(
											(energyData.total_value / 200) * 100,
											100
										).toFixed(0)}
										%
									</span>
								</div>
							</div>
						</div>
						<div className="stat-card-body">
							<div className="stat-label">Energy</div>
							<div className="stat-value">
								{energyData.total_value.toFixed(1)} kWh
							</div>
							<div className="stat-meta">Now: {energyData.count} entries</div>
						</div>
					</div>

					<div className="stat-card">
						<div className="stat-card-header">
							<div
								className="stat-icon"
								style={{ background: "#f3e5f5" }}>
								<Database
									size={24}
									style={{ color: "#8b5cf6" }}
								/>
							</div>
							<div className="stat-progress">
								<div className="progress-ring">
									<svg
										width="60"
										height="60">
										<circle
											cx="30"
											cy="30"
											r="26"
											fill="none"
											stroke="#e0e0e0"
											strokeWidth="4"
										/>
										<circle
											cx="30"
											cy="30"
											r="26"
											fill="none"
											stroke="#8b5cf6"
											strokeWidth="4"
											strokeDasharray={`${(digitalData.total_value / 100) * 163} 163`}
											transform="rotate(-90 30 30)"
										/>
									</svg>
									<span className="progress-text">
										{Math.min(
											(digitalData.total_value / 100) * 100,
											100
										).toFixed(0)}
										%
									</span>
								</div>
							</div>
						</div>
						<div className="stat-card-body">
							<div className="stat-label">Digital</div>
							<div className="stat-value">
								{digitalData.total_value.toFixed(1)} GB
							</div>
							<div className="stat-meta">Now: {digitalData.count} entries</div>
						</div>
					</div>
				</div>

				{/* Advanced Visualizations */}
				{stats.metric_breakdown && stats.metric_breakdown.length > 0 && (
					<div className="visualizations-section">
						<div className="section-header">
							<h2>Impact Visualizations</h2>
						</div>
						<div className="charts-grid advanced-charts">
							{/* Carbon Progress Ring (Radial Bar Chart) */}
							<div className="chart-card advanced-chart">
								<div className="chart-header">
									<Wind
										className="chart-icon"
										size={24}
									/>
									<h3>Carbon Footprint</h3>
								</div>
								<div className="radial-chart-container">
									<ResponsiveContainer
										width="100%"
										height={300}>
										<RadialBarChart
											innerRadius="60%"
											outerRadius="100%"
											data={radialData}
											startAngle={180}
											endAngle={0}>
											<PolarGrid gridType="circle" />
											<PolarAngleAxis
												type="number"
												domain={[0, 100]}
												tick={false}
											/>
											<RadialBar
												background
												dataKey="value"
												cornerRadius={10}
												fill="#10b981"
											/>
											<Tooltip content={<CustomTooltip />} />
										</RadialBarChart>
									</ResponsiveContainer>
									<div className="chart-stats">
										<p className="chart-stat-large">
											{carbonData.total_value.toFixed(1)} kg
										</p>
										<p className="chart-stat-small">
											of {carbonGoal} kg goal ({carbonProgress.toFixed(1)}%)
										</p>
										<div className="chart-stat-grid">
											<div className="chart-stat-item">
												<p className="stat-label-small">Average</p>
												<p className="stat-value-small">
													{carbonData.avg_value.toFixed(2)} kg
												</p>
											</div>
											<div className="chart-stat-item">
												<p className="stat-label-small">Entries</p>
												<p className="stat-value-small">{carbonData.count}</p>
											</div>
										</div>
									</div>
								</div>
							</div>

							{/* Water Usage Treemap */}
							<div className="chart-card advanced-chart">
								<div className="chart-header">
									<Droplets
										className="chart-icon"
										size={24}
									/>
									<h3>Water Usage</h3>
								</div>
								<ResponsiveContainer
									width="100%"
									height={300}>
									<Treemap
										data={treemapData}
										dataKey="size"
										aspectRatio={4 / 3}
										stroke="#fff"
										fill="#06b6d4">
										<Tooltip content={<CustomTooltip />} />
									</Treemap>
								</ResponsiveContainer>
								<div className="chart-stats-grid">
									<div className="chart-stat-item">
										<p className="stat-label-small">Total</p>
										<p className="stat-value-small">
											{waterData.total_value.toFixed(1)} L
										</p>
									</div>
									<div className="chart-stat-item">
										<p className="stat-label-small">Average</p>
										<p className="stat-value-small">
											{waterData.avg_value.toFixed(2)} L
										</p>
									</div>
									<div className="chart-stat-item">
										<p className="stat-label-small">Entries</p>
										<p className="stat-value-small">{waterData.count}</p>
									</div>
								</div>
							</div>

							{/* Energy & Digital Bubble Chart
							<div className="chart-card advanced-chart">
								<div className="chart-header">
									<Zap
										className="chart-icon"
										size={24}
									/>
									<h3>Energy & Digital Impact</h3>
								</div>
								<ResponsiveContainer
									width="100%"
									height={300}>
									<ScatterChart
										margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
										<CartesianGrid strokeDasharray="3 3" />
										<XAxis
											type="number"
											dataKey="x"
											name="Entries"
											label={{
												value: "Number of Entries",
												position: "insideBottom",
												offset: -10,
											}}
										/>
										<YAxis
											type="number"
											dataKey="y"
											name="Average"
											label={{
												value: "Average Value",
												angle: -90,
												position: "insideLeft",
											}}
										/>
										<ZAxis
											type="number"
											dataKey="z"
											range={[100, 1000]}
											name="Total"
										/>
										<Tooltip
											content={<CustomTooltip />}
											cursor={{ strokeDasharray: "3 3" }}
										/>
										<Legend />
										<Scatter
											name="Energy"
											data={[bubbleData[0]]}
											fill="#fbbf24">
											<Cell fill="#fbbf24" />
										</Scatter>
										<Scatter
											name="Digital"
											data={[bubbleData[1]]}
											fill="#8b5cf6">
											<Cell fill="#8b5cf6" />
										</Scatter>
									</ScatterChart>
								</ResponsiveContainer>
								<div className="chart-stats-grid">
									<div className="chart-stat-item">
										<p className="stat-label-small">Energy</p>
										<p className="stat-value-small">
											Total: {energyData.total_value.toFixed(1)} kWh
										</p>
										<p className="stat-value-small">
											Avg: {energyData.avg_value.toFixed(2)} kWh
										</p>
									</div>
									<div className="chart-stat-item">
										<p className="stat-label-small">Digital</p>
										<p className="stat-value-small">
											Total: {digitalData.total_value.toFixed(1)} GB
										</p>
										<p className="stat-value-small">
											Avg: {digitalData.avg_value.toFixed(2)} GB
										</p>
									</div>
								</div>
							</div> */}

							{/* Activity Timeline (Line Chart) */}
							<div className="chart-card advanced-chart">
								<div className="chart-header">
									<Activity
										className="chart-icon"
										size={24}
									/>
									<h3>Weekly Activity</h3>
								</div>
								<ResponsiveContainer
									width="100%"
									height={300}>
									<LineChart data={activityData}>
										<CartesianGrid
											strokeDasharray="3 3"
											stroke="#e5e7eb"
										/>
										<XAxis
											dataKey="day"
											stroke="#6b7280"
										/>
										<YAxis stroke="#6b7280" />
										<Tooltip content={<CustomTooltip />} />
										<Legend />
										<Line
											type="monotone"
											dataKey="entries"
											stroke="#6366f1"
											strokeWidth={3}
											dot={{ fill: "#6366f1", r: 6 }}
											activeDot={{ r: 8 }}
											name="Entries"
										/>
									</LineChart>
								</ResponsiveContainer>
								<div className="chart-insight">
									<p className="insight-text">
										<span className="insight-bold">Insight:</span> Track your
										entries consistently to see patterns in your environmental
										impact.
									</p>
								</div>
							</div>
						</div>
					</div>
				)}

				{/* Performance Chart */}
				{performanceData.length > 0 && (
					<div className="chart-section">
						<div className="section-header">
							<h2>Performance Over Time</h2>
							<span className="date-range">1 Aug 2023 - 31 Aug 2024</span>
						</div>
						<div className="chart-card">
							<div className="chart-legend">
								<span className="legend-item">
									<span
										className="legend-dot"
										style={{ background: "#10b981" }}></span>{" "}
									Carbon
								</span>
								<span className="legend-item">
									<span
										className="legend-dot"
										style={{ background: "#3b82f6" }}></span>{" "}
									Water
								</span>
								<span className="legend-item">
									<span
										className="legend-dot"
										style={{ background: "#f59e0b" }}></span>{" "}
									Energy
								</span>
								<span className="legend-item">
									<span
										className="legend-dot"
										style={{ background: "#8b5cf6" }}></span>{" "}
									Digital
								</span>
							</div>
							<ResponsiveContainer
								width="100%"
								height={350}>
								<BarChart data={performanceData}>
									<CartesianGrid
										strokeDasharray="3 3"
										stroke="#f0f0f0"
										vertical={false}
									/>
									<XAxis
										dataKey="month"
										tick={{ fill: "#666", fontSize: 12 }}
									/>
									<YAxis tick={{ fill: "#666", fontSize: 12 }} />
									<Tooltip content={<CustomTooltip />} />
									<Bar
										dataKey="Carbon"
										stackId="a"
										fill="#10b981"
										radius={[0, 0, 0, 0]}
									/>
									<Bar
										dataKey="Water"
										stackId="a"
										fill="#3b82f6"
										radius={[0, 0, 0, 0]}
									/>
									<Bar
										dataKey="Energy"
										stackId="a"
										fill="#f59e0b"
										radius={[0, 0, 0, 0]}
									/>
									<Bar
										dataKey="Digital"
										stackId="a"
										fill="#8b5cf6"
										radius={[4, 4, 0, 0]}
									/>
								</BarChart>
							</ResponsiveContainer>
						</div>
					</div>
				)}

				{/* Entries Section */}
				<div className="entries-section">
					<div className="section-header">
						<h2>Recent Entries</h2>
						<div className="section-actions">
							<select
								value={filterMetric}
								onChange={(e) => setFilterMetric(e.target.value)}
								disabled={filtering}
								className="filter-select">
								<option value="all">All Metrics</option>
								<option value="carbon">Carbon</option>
								<option value="water">Water</option>
								<option value="energy">Energy</option>
								<option value="digital">Digital</option>
							</select>
							<button
								onClick={() => setShowAddModal(true)}
								className="btn-add">
								+ Add Entry
							</button>
						</div>
					</div>

					{entries.length === 0 ? (
						<div className="empty-state">
							<Leaf
								size={48}
								style={{ color: "#cbd5e0" }}
							/>
							<p>No entries yet. Start tracking your environmental impact!</p>
							<button
								onClick={() => setShowAddModal(true)}
								className="btn-primary">
								Add Your First Entry
							</button>
						</div>
					) : (
						<div className="entries-grid">
							{entries.map((entry) => (
								<div
									key={entry.id}
									className="entry-card"
									onClick={() => handleEntryClick(entry)}>
									<div className="entry-header">
										<div
											className="entry-icon"
											style={{
												background: `${getMetricColor(entry.metric_type)}15`,
											}}>
											{getMetricIcon(entry.metric_type)}
										</div>
										<span
											className="entry-type"
											style={{ color: getMetricColor(entry.metric_type) }}>
											{entry.metric_type.charAt(0).toUpperCase() +
												entry.metric_type.slice(1)}
										</span>
									</div>
									<div className="entry-value">{entry.value}</div>
									<div className="entry-description">{entry.description}</div>
									<div className="entry-footer">
										<span className="entry-date">
											{new Date(entry.created_at).toLocaleDateString()}
										</span>
										<button
											onClick={(e) => {
												e.stopPropagation();
												handleDeleteEntry(entry.id);
											}}
											className="btn-delete-icon">
											×
										</button>
									</div>
								</div>
							))}
						</div>
					)}
				</div>
			</div>

			{/* Add Entry Modal */}
			{showAddModal && (
				<div
					className="modal-overlay"
					onClick={() => setShowAddModal(false)}>
					<div
						className="modal-card"
						onClick={(e) => e.stopPropagation()}>
						<div className="modal-header">
							<h2>Add New Entry</h2>
							<button
								className="modal-close"
								onClick={() => setShowAddModal(false)}>
								×
							</button>
						</div>
						<form
							onSubmit={handleAddEntry}
							className="modal-form">
							<div className="form-group">
								<label>Metric Type</label>
								<select
									value={newEntry.metric_type}
									onChange={(e) =>
										setNewEntry({ ...newEntry, metric_type: e.target.value })
									}
									required>
									<option value="carbon">Carbon Footprint</option>
									<option value="water">Water Usage</option>
									<option value="energy">Energy Consumption</option>
									<option value="digital">Digital Usage</option>
								</select>
							</div>
							<div className="form-group">
								<label>Value</label>
								<input
									type="number"
									step="0.01"
									value={newEntry.value}
									onChange={(e) =>
										setNewEntry({ ...newEntry, value: e.target.value })
									}
									required
									placeholder="Enter value"
								/>
							</div>
							<div className="form-group">
								<label>Description</label>
								<textarea
									value={newEntry.description}
									onChange={(e) =>
										setNewEntry({ ...newEntry, description: e.target.value })
									}
									placeholder="Describe this entry..."
									rows="3"
								/>
							</div>
							<div className="modal-actions">
								<button
									type="button"
									onClick={() => setShowAddModal(false)}
									className="btn-secondary">
									Cancel
								</button>
								<button
									type="submit"
									className="btn-primary">
									Add Entry
								</button>
							</div>
						</form>
					</div>
				</div>
			)}

			{/* Entry Detail Modal */}
			{showDetailModal && selectedEntry && (
				<div
					className="modal-overlay"
					onClick={() => setShowDetailModal(false)}>
					<div
						className="modal-card"
						onClick={(e) => e.stopPropagation()}>
						<div className="modal-header">
							<h2>Entry Details</h2>
							<button
								className="modal-close"
								onClick={() => setShowDetailModal(false)}>
								×
							</button>
						</div>
						<div className="detail-content">
							<div className="detail-row">
								<div className="detail-label">Metric Type</div>
								<div className="detail-value">
									{selectedEntry.metric_type.charAt(0).toUpperCase() +
										selectedEntry.metric_type.slice(1)}
								</div>
							</div>
							<div className="detail-row">
								<div className="detail-label">Value</div>
								<div className="detail-value">{selectedEntry.value}</div>
							</div>
							<div className="detail-row">
								<div className="detail-label">Description</div>
								<div className="detail-value">{selectedEntry.description}</div>
							</div>
							<div className="detail-row">
								<div className="detail-label">Created</div>
								<div className="detail-value">
									{new Date(selectedEntry.created_at).toLocaleString()}
								</div>
							</div>
						</div>
						<div className="modal-actions">
							<button
								onClick={() => setShowDetailModal(false)}
								className="btn-secondary">
								Close
							</button>
						</div>
					</div>
				</div>
			)}
		</div>
	);
};

export default Dashboard;

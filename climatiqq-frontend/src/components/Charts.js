import React, { useState } from 'react';
import './Charts.css';

const Charts = ({ entries, stats, darkMode = false }) => {
  // Safety checks to prevent undefined access errors
  const safeEntries = entries || [];
  const safeStats = stats || {};

  const [selectedTimeframe, setSelectedTimeframe] = useState('7d');
  const [selectedMetric, setSelectedMetric] = useState('all');

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const formatDateFull = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', { 
      weekday: 'short',
      month: 'short', 
      day: 'numeric' 
    });
  };

  const getChartData = (timeframe = '7d') => {
    if (!safeEntries || safeEntries.length === 0) return [];
    
    const now = new Date();
    let cutoffDate;
    
    switch(timeframe) {
      case '7d':
        cutoffDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        break;
      case '30d':
        cutoffDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        break;
      case '90d':
        cutoffDate = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000);
        break;
      default:
        cutoffDate = new Date(0);
    }
    
    // Filter entries by timeframe
    const filteredEntries = safeEntries.filter(entry => 
      new Date(entry.created_at) >= cutoffDate
    );
    
    // Group entries by date
    const groupedByDate = filteredEntries.reduce((acc, entry) => {
      const date = formatDate(entry.created_at);
      if (!acc[date]) {
        acc[date] = { carbon: 0, water: 0, energy: 0, digital: 0 };
      }
      acc[date][entry.metric_type] += parseFloat(entry.value);
      return acc;
    }, {});

    return Object.entries(groupedByDate).map(([date, values]) => ({
      date,
      carbon: values.carbon,
      water: values.water,
      energy: values.energy,
      digital: values.digital,
      total: values.carbon + values.water + values.energy + values.digital
    }));
  };

  const getCategoryBreakdown = () => {
    if (!safeEntries || safeEntries.length === 0) return [];
    
    const breakdown = safeEntries.reduce((acc, entry) => {
      const category = entry.metric_type;
      if (!acc[category]) acc[category] = 0;
      acc[category] += parseFloat(entry.value);
      return acc;
    }, {});

    return Object.entries(breakdown).map(([category, value]) => ({
      category: category.charAt(0).toUpperCase() + category.slice(1),
      value: parseFloat(value.toFixed(2)),
      percentage: ((value / Object.values(breakdown).reduce((a, b) => a + b, 0)) * 100).toFixed(1)
    }));
  };

  const getTrendData = () => {
    const data = getChartData(selectedTimeframe);
    return data.slice(-7); // Last 7 days
  };

  const getMetricData = () => {
    const data = getChartData(selectedTimeframe);
    if (selectedMetric === 'all') return data;
    
    return data.map(day => ({
      date: day.date,
      value: day[selectedMetric] || 0
    }));
  };

  const chartData = getChartData();
  const categoryBreakdown = getCategoryBreakdown();
  const trendData = getTrendData();
  const metricData = getMetricData();

  const getBarColor = (category) => {
    const colors = {
      carbon: '#10b981',
      water: '#3b82f6',
      energy: '#f59e0b',
      digital: '#8b5cf6'
    };
    return colors[category.toLowerCase()] || '#6b7280';
  };

  const getCategoryColor = (category) => {
    const colors = {
      Carbon: '#10b981',
      Water: '#3b82f6',
      Energy: '#f59e0b',
      Digital: '#8b5cf6'
    };
    return colors[category] || '#6b7280';
  };

  const getMaxValue = (data, metric = 'total') => {
    if (!data || data.length === 0) return 1;
    return Math.max(...data.map(item => item[metric] || 0));
  };

  const calculatePercentage = (value, maxValue) => {
    return maxValue > 0 ? (value / maxValue) * 100 : 0;
  };

  const getInsights = () => {
    if (!safeEntries || safeEntries.length === 0) return [];
    
    const insights = [];
    const totalCarbon = safeEntries.reduce((sum, entry) => 
      entry.metric_type === 'carbon' ? sum + parseFloat(entry.value) : sum, 0
    );
    const totalWater = safeEntries.reduce((sum, entry) => 
      entry.metric_type === 'water' ? sum + parseFloat(entry.value) : sum, 0
    );
    const totalEnergy = safeEntries.reduce((sum, entry) => 
      entry.metric_type === 'energy' ? sum + parseFloat(entry.value) : sum, 0
    );

    // Carbon insights
    if (totalCarbon > 0) {
      const treesNeeded = Math.ceil(totalCarbon / 22); // 1 tree absorbs ~22kg CO2/year
      insights.push({
        type: 'carbon',
        title: 'Carbon Offset',
        value: `${treesNeeded} trees`,
        description: `You'd need ${treesNeeded} trees to offset your carbon footprint`,
        icon: '🌳'
      });
    }

    // Water insights
    if (totalWater > 0) {
      const showers = Math.round(totalWater / 65); // Average shower uses 65L
      insights.push({
        type: 'water',
        title: 'Water Usage',
        value: `${showers} showers`,
        description: `Your water usage equals ${showers} average showers`,
        icon: '🚿'
      });
    }

    // Energy insights
    if (totalEnergy > 0) {
      const hours = Math.round(totalEnergy * 10); // Rough conversion
      insights.push({
        type: 'energy',
        title: 'Energy Impact',
        value: `${hours} hours`,
        description: `Your energy usage equals ${hours} hours of device usage`,
        icon: '⚡'
      });
    }

    return insights;
  };

  const getProgressData = () => {
    if (!safeEntries || safeEntries.length === 0) return null;
    
    const totalEntries = safeEntries.length;
    
    // Get current week (Monday to Sunday)
    const now = new Date();
    const startOfWeek = new Date(now);
    startOfWeek.setDate(now.getDate() - now.getDay() + 1); // Monday
    startOfWeek.setHours(0, 0, 0, 0);
    
    const endOfWeek = new Date(startOfWeek);
    endOfWeek.setDate(startOfWeek.getDate() + 6); // Sunday
    endOfWeek.setHours(23, 59, 59, 999);
    
    // Count entries from this week
    const thisWeekEntries = safeEntries.filter(entry => {
      const entryDate = new Date(entry.created_at);
      return entryDate >= startOfWeek && entryDate <= endOfWeek;
    }).length;
    
    // Calculate days since start of week
    const daysSinceStart = Math.min(Math.floor((now - startOfWeek) / (1000 * 60 * 60 * 24)) + 1, 7);
    
    // Calculate progress based on entries vs days
    const weeklyGoal = 7; // Goal: 7 entries per week
    const progressPercentage = Math.min((thisWeekEntries / weeklyGoal) * 100, 100);
    
    // Alternative: progress based on days with entries
    const uniqueDaysThisWeek = new Set(
      safeEntries
        .filter(entry => {
          const entryDate = new Date(entry.created_at);
          return entryDate >= startOfWeek && entryDate <= endOfWeek;
        })
        .map(entry => new Date(entry.created_at).toDateString())
    ).size;
    
    const daysProgress = Math.min((uniqueDaysThisWeek / 7) * 100, 100);

    return {
      totalEntries,
      thisWeek: thisWeekEntries,
      uniqueDays: uniqueDaysThisWeek,
      daysSinceStart,
      weeklyGoal,
      weeklyProgress: progressPercentage,
      daysProgress: daysProgress,
      startOfWeek: startOfWeek.toLocaleDateString(),
      endOfWeek: endOfWeek.toLocaleDateString()
    };
  };

  const progressData = getProgressData();
  const insights = getInsights();

  return (
    <div className={`charts-container ${darkMode ? 'dark' : ''}`}>
      {/* Advanced Analytics Header */}
      <div className="analytics-header">
        <h2>Advanced Analytics</h2>
        <p>Track your environmental impact with detailed insights and trends</p>
      </div>

      {/* Progress Overview */}
      {progressData && (
        <div className="progress-section">
          <div className="progress-card">
            <div className="progress-header">
              <h3>Weekly Progress</h3>
              <span className="progress-icon">📊</span>
            </div>
            <div className="progress-bar">
              <div 
                className="progress-fill"
                style={{ width: `${progressData.weeklyProgress}%` }}
              ></div>
            </div>
            <div className="progress-stats">
              <span>{progressData.thisWeek} entries this week</span>
              <span>{progressData.uniqueDays}/7 days with entries</span>
              <span>{progressData.weeklyProgress.toFixed(0)}% of weekly goal</span>
            </div>
            <div className="progress-details">
              <small>Week: {progressData.startOfWeek} - {progressData.endOfWeek}</small>
              <small>Goal: 7 entries per week</small>
            </div>
          </div>
        </div>
      )}

      {/* Insights Cards */}
      {insights.length > 0 && (
        <div className="insights-section">
          <h3>Environmental Insights</h3>
          <div className="insights-grid">
            {insights.map((insight, index) => (
              <div key={index} className={`insight-card ${insight.type}`}>
                <div className="insight-icon">{insight.icon}</div>
                <div className="insight-content">
                  <h4>{insight.title}</h4>
                  <div className="insight-value">{insight.value}</div>
                  <p>{insight.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Enhanced Category Breakdown */}
      <div className="chart-section">
        <h3>Impact Distribution</h3>
        <div className="category-breakdown">
          {categoryBreakdown.map((item, index) => (
            <div key={index} className="category-item">
              <div className="category-header">
                <span 
                  className="category-color" 
                  style={{ backgroundColor: getCategoryColor(item.category) }}
                ></span>
                <span className="category-name">{item.category}</span>
                <span className="category-percentage">{item.percentage}%</span>
              </div>
              <div className="category-bar">
                <div 
                  className="category-fill"
                  style={{ 
                    width: `${item.percentage}%`,
                    backgroundColor: getCategoryColor(item.category)
                  }}
                ></div>
              </div>
              <div className="category-value">{item.value}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Enhanced Trend Chart */}
      <div className="chart-section">
        <div className="chart-header">
          <h3>Trend Analysis</h3>
          <div className="chart-controls">
            <select 
              value={selectedTimeframe} 
              onChange={(e) => setSelectedTimeframe(e.target.value)}
              className="timeframe-select"
            >
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
            </select>
            <select 
              value={selectedMetric} 
              onChange={(e) => setSelectedMetric(e.target.value)}
              className="metric-select"
            >
              <option value="all">All Metrics</option>
              <option value="carbon">Carbon</option>
              <option value="water">Water</option>
              <option value="energy">Energy</option>
            </select>
          </div>
        </div>
        <div className="trend-chart">
          {metricData.map((day, index) => {
            const maxValue = getMaxValue(metricData, selectedMetric === 'all' ? 'total' : selectedMetric);
            const percentage = calculatePercentage(
              selectedMetric === 'all' ? day.total : day.value, 
              maxValue
            );
            
            return (
              <div key={index} className="trend-day">
                <div className="trend-date">{day.date}</div>
                <div className="trend-bar-container">
                  <div 
                    className={`trend-bar ${selectedMetric === 'all' ? 'multi' : selectedMetric}`}
                    style={{ height: `${percentage}%` }}
                    title={`${selectedMetric === 'all' ? 'Total' : selectedMetric.charAt(0).toUpperCase() + selectedMetric.slice(1)}: ${selectedMetric === 'all' ? day.total : day.value}`}
                  >
                    {selectedMetric === 'all' && (
                      <>
                        {day.carbon > 0 && (
                          <div 
                            className="trend-segment carbon"
                            style={{ height: `${calculatePercentage(day.carbon, maxValue)}%` }}
                          ></div>
                        )}
                        {day.water > 0 && (
                          <div 
                            className="trend-segment water"
                            style={{ height: `${calculatePercentage(day.water, maxValue)}%` }}
                          ></div>
                        )}
                        {day.energy > 0 && (
                          <div 
                            className="trend-segment energy"
                            style={{ height: `${calculatePercentage(day.energy, maxValue)}%` }}
                          ></div>
                        )}
                      </>
                    )}
                  </div>
                </div>
                <div className="trend-value">
                  {(selectedMetric === 'all' ? day.total : day.value).toFixed(1)}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Enhanced Summary Stats */}
      <div className="chart-section">
        <h3>Summary Statistics</h3>
        <div className="summary-stats">
          <div className="stat-item">
            <div className="stat-icon">📊</div>
            <div className="stat-number">{safeStats?.total_entries || safeEntries?.length || 0}</div>
            <div className="stat-label">Total Entries</div>
          </div>
          <div className="stat-item">
            <div className="stat-icon">🌱</div>
            <div className="stat-number">
              {chartData.reduce((sum, day) => sum + day.carbon, 0).toFixed(1)}
            </div>
            <div className="stat-label">Carbon (kg)</div>
          </div>
          <div className="stat-item">
            <div className="stat-icon">💧</div>
            <div className="stat-number">
              {chartData.reduce((sum, day) => sum + day.water, 0).toFixed(1)}
            </div>
            <div className="stat-label">Water (L)</div>
          </div>
          <div className="stat-item">
            <div className="stat-icon">⚡</div>
            <div className="stat-number">
              {chartData.reduce((sum, day) => sum + day.energy, 0).toFixed(1)}
            </div>
            <div className="stat-label">Energy (kWh)</div>
          </div>
          <div className="stat-item">
            <div className="stat-icon">📅</div>
            <div className="stat-number">
              {chartData.length}
            </div>
            <div className="stat-label">Days Tracked</div>
          </div>
          <div className="stat-item">
            <div className="stat-icon">📈</div>
            <div className="stat-number">
              {(chartData.reduce((sum, day) => sum + day.total, 0) / Math.max(chartData.length, 1)).toFixed(1)}
            </div>
            <div className="stat-label">Daily Average</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Charts; 
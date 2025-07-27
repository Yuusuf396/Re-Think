import React, { useState, useEffect } from 'react';
import Charts from './Charts';
import apiService from '../services/api';
import './Dashboard.css';

const Dashboard = ({ token, darkMode }) => {
    const [entries, setEntries] = useState([]);
    const [stats, setStats] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [showAddModal, setShowAddModal] = useState(false);
    const [showDetailModal, setShowDetailModal] = useState(false);
    const [selectedEntry, setSelectedEntry] = useState(null);
    const [newEntry, setNewEntry] = useState({
        metric_type: 'carbon',
        value: '',
        description: ''
    });

    useEffect(() => {
        fetchData();
    }, [token]);

    const fetchData = async () => {
        try {
            setLoading(true);
            
            // Fetch entries and stats in parallel
            const [entriesResponse, statsResponse] = await Promise.all([
                apiService.entries.getAll(),
                apiService.stats.getImpactStats()
            ]);

            setEntries(entriesResponse);
            setStats(statsResponse);
            setError('');
        } catch (error) {
            console.error('Dashboard fetch error:', error);
            setError('Failed to load dashboard data. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleAddEntry = async (e) => {
        e.preventDefault();
        
        try {
            const response = await apiService.entries.create(newEntry);
            setEntries([response, ...entries]);
            setShowAddModal(false);
            setNewEntry({ metric_type: 'carbon', value: '', description: '' });
            
            // Refresh stats
            const updatedStats = await apiService.stats.getImpactStats();
            setStats(updatedStats);
        } catch (error) {
            console.error('Add entry error:', error);
            setError('Failed to add entry. Please try again.');
        }
    };

    const handleDeleteEntry = async (id) => {
        if (window.confirm('Are you sure you want to delete this entry?')) {
            try {
                await apiService.entries.delete(id);
                setEntries(entries.filter(entry => entry.id !== id));
                
                // Refresh stats
                const updatedStats = await apiService.stats.getImpactStats();
                setStats(updatedStats);
            } catch (error) {
                console.error('Delete entry error:', error);
                setError('Failed to delete entry. Please try again.');
            }
        }
    };

    const handleEntryClick = (entry) => {
        setSelectedEntry(entry);
        setShowDetailModal(true);
    };

    const getMetricIcon = (metricType) => {
        const icons = {
            carbon: '🌱',
            water: '💧',
            energy: '⚡',
            digital: '💻'
        };
        return icons[metricType] || '📊';
    };

    const getMetricColor = (metricType) => {
        const colors = {
            carbon: '#10b981',
            water: '#3b82f6',
            energy: '#f59e0b',
            digital: '#8b5cf6'
        };
        return colors[metricType] || '#6b7280';
    };

    if (loading) {
        return (
            <div className={`dashboard ${darkMode ? 'dark' : ''}`}>
                <div className="main-content">
                    <div className="loading">Loading dashboard...</div>
                </div>
            </div>
        );
    }

    return (
        <div className={`dashboard ${darkMode ? 'dark' : ''}`}>
            <div className="main-content">
                {/* Stats Overview */}
                <div className="stats-overview">
                    <h1>Welcome to Rethink</h1>
                    <p>Track your environmental impact and get personalized insights</p>
                    
                    {error && <div className="error">{error}</div>}
                    
                    <div className="stats-grid">
                        <div className="stat-card">
                            <div className="stat-icon">🌱</div>
                            <div className="stat-number">{stats.total_carbon || 0}</div>
                            <div className="stat-label">Total Carbon (kg CO2)</div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-icon">💧</div>
                            <div className="stat-number">{stats.total_water || 0}</div>
                            <div className="stat-label">Total Water (L)</div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-icon">⚡</div>
                            <div className="stat-number">{stats.total_energy || 0}</div>
                            <div className="stat-label">Total Energy (kWh)</div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-icon">📊</div>
                            <div className="stat-number">{entries.length}</div>
                            <div className="stat-label">Total Entries</div>
                        </div>
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="quick-actions">
                    <h2>Quick Actions</h2>
                    <button 
                        onClick={() => setShowAddModal(true)}
                        className="btn-add-entry"
                    >
                        + Add New Entry
                    </button>
                </div>

                {/* Entries Section */}
                <div className="entries-section">
                    <h2>Recent Entries</h2>
                    {entries.length === 0 ? (
                        <div className="empty-state">
                            <p>No entries yet. Start tracking your environmental impact!</p>
                        </div>
                    ) : (
                        <div className="entries-grid">
                            {entries.map(entry => (
                                <div 
                                    key={entry.id} 
                                    className="entry-card"
                                    onClick={() => handleEntryClick(entry)}
                                >
                                    <div className="entry-header">
                                        <span className="entry-icon">
                                            {getMetricIcon(entry.metric_type)}
                                        </span>
                                        <span 
                                            className="entry-metric"
                                            style={{ color: getMetricColor(entry.metric_type) }}
                                        >
                                            {entry.metric_type.charAt(0).toUpperCase() + entry.metric_type.slice(1)}
                                        </span>
                                    </div>
                                    <div className="entry-value">{entry.value}</div>
                                    <div className="entry-description">{entry.description}</div>
                                    <div className="entry-date">
                                        {new Date(entry.created_at).toLocaleDateString()}
                                    </div>
                                    <button 
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            handleDeleteEntry(entry.id);
                                        }}
                                        className="btn-delete"
                                    >
                                        Delete
                                    </button>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Charts Section */}
                <Charts entries={entries} darkMode={darkMode} />

                {/* Coming Soon Section */}
                <div className="coming-soon-section">
                    <h3>🚀 Coming Soon</h3>
                    <div className="coming-soon-grid">
                        <div className="coming-soon-item">
                            <div className="coming-soon-icon">📧</div>
                            <div className="coming-soon-content">
                                <h4>Email Notifications</h4>
                                <p>Password reset and email verification</p>
                            </div>
                        </div>
                        <div className="coming-soon-item">
                            <div className="coming-soon-icon">📱</div>
                            <div className="coming-soon-content">
                                <h4>Mobile App</h4>
                                <p>Track your impact on the go</p>
                            </div>
                        </div>
                        <div className="coming-soon-item">
                            <div className="coming-soon-icon">🤝</div>
                            <div className="coming-soon-content">
                                <h4>Social Features</h4>
                                <p>Share achievements with friends</p>
                            </div>
                        </div>
                        <div className="coming-soon-item">
                            <div className="coming-soon-icon">📊</div>
                            <div className="coming-soon-content">
                                <h4>Advanced Analytics</h4>
                                <p>Detailed insights and trends</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Add Entry Modal */}
            {showAddModal && (
                <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
                    <div className="modal" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2>Add New Entry</h2>
                            <button 
                                className="modal-close"
                                onClick={() => setShowAddModal(false)}
                            >
                                ×
                            </button>
                        </div>
                        <form onSubmit={handleAddEntry}>
                            <div className="form-group">
                                <label>Metric Type</label>
                                <select
                                    value={newEntry.metric_type}
                                    onChange={(e) => setNewEntry({
                                        ...newEntry,
                                        metric_type: e.target.value
                                    })}
                                    required
                                >
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
                                    onChange={(e) => setNewEntry({
                                        ...newEntry,
                                        value: e.target.value
                                    })}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Description</label>
                                <textarea
                                    value={newEntry.description}
                                    onChange={(e) => setNewEntry({
                                        ...newEntry,
                                        description: e.target.value
                                    })}
                                    placeholder="Describe this entry..."
                                />
                            </div>
                            <div className="modal-actions">
                                <button type="button" onClick={() => setShowAddModal(false)}>
                                    Cancel
                                </button>
                                <button type="submit">Add Entry</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Entry Detail Modal */}
            {showDetailModal && selectedEntry && (
                <div className="modal-overlay" onClick={() => setShowDetailModal(false)}>
                    <div className="detail-modal" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2>Entry Details</h2>
                            <button 
                                className="modal-close"
                                onClick={() => setShowDetailModal(false)}
                            >
                                ×
                            </button>
                        </div>
                        <div className="detail-content">
                            <div className="detail-section">
                                <h3>Metric Type</h3>
                                <div className="detail-value">
                                    {selectedEntry.metric_type.charAt(0).toUpperCase() + selectedEntry.metric_type.slice(1)}
                                </div>
                            </div>
                            <div className="detail-section">
                                <h3>Value</h3>
                                <div className="detail-value">{selectedEntry.value}</div>
                            </div>
                            <div className="detail-section">
                                <h3>Description</h3>
                                <div className="impact-description">{selectedEntry.description}</div>
                            </div>
                            <div className="detail-section">
                                <h3>Created</h3>
                                <div className="detail-value">
                                    {new Date(selectedEntry.created_at).toLocaleString()}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard; 
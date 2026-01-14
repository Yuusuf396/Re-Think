-- ============================================================================
-- Climatiqq PostgreSQL Database Schema
-- ============================================================================
-- This file contains the raw SQL schema matching the Django models.
-- Run this to create the database schema directly in PostgreSQL.
--
-- Usage:
--   psql -U postgres -d climatiqq -f scripts/schema.sql
--   Or from psql prompt: \i scripts/schema.sql
-- ============================================================================

-- Enable UUID extension if needed (for future use)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- Django Auth User Table
-- ============================================================================
-- Standard Django user model table
-- This matches django.contrib.auth.models.User

CREATE TABLE IF NOT EXISTS auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for auth_user
CREATE INDEX IF NOT EXISTS auth_user_username_idx ON auth_user(username);
CREATE INDEX IF NOT EXISTS auth_user_email_idx ON auth_user(email);

-- Comments for auth_user table
COMMENT ON TABLE auth_user IS 'Django authentication user table';
COMMENT ON COLUMN auth_user.id IS 'Primary key - auto-incrementing integer';
COMMENT ON COLUMN auth_user.username IS 'Unique username for login';
COMMENT ON COLUMN auth_user.email IS 'User email address (used for login in this app)';
COMMENT ON COLUMN auth_user.password IS 'Hashed password (never stored in plain text)';
COMMENT ON COLUMN auth_user.is_active IS 'Designates whether this user should be treated as active';
COMMENT ON COLUMN auth_user.date_joined IS 'Date and time when user account was created';

-- ============================================================================
-- Impact Entry Table
-- ============================================================================
-- Tracks user environmental impact entries
-- This matches tracker.models.ImpactEntry

CREATE TABLE IF NOT EXISTS tracker_impactentry (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    metric_type VARCHAR(20) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    description VARCHAR(200) DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    CONSTRAINT tracker_impactentry_user_id_fk 
        FOREIGN KEY (user_id) 
        REFERENCES auth_user(id) 
        ON DELETE CASCADE,
    
    -- Check constraint for metric_type choices
    CONSTRAINT tracker_impactentry_metric_type_check 
        CHECK (metric_type IN ('carbon', 'water', 'energy', 'digital'))
);

-- Indexes for tracker_impactentry
CREATE INDEX IF NOT EXISTS tracker_impactentry_user_id_idx 
    ON tracker_impactentry(user_id);
CREATE INDEX IF NOT EXISTS tracker_impactentry_created_at_idx 
    ON tracker_impactentry(created_at DESC);
CREATE INDEX IF NOT EXISTS tracker_impactentry_metric_type_idx 
    ON tracker_impactentry(metric_type);

-- Comments for tracker_impactentry table
COMMENT ON TABLE tracker_impactentry IS 'Stores user environmental impact entries';
COMMENT ON COLUMN tracker_impactentry.id IS 'Primary key - auto-incrementing big integer';
COMMENT ON COLUMN tracker_impactentry.user_id IS 'Foreign key to auth_user - links entry to user';
COMMENT ON COLUMN tracker_impactentry.metric_type IS 'Type of metric: carbon, water, energy, or digital';
COMMENT ON COLUMN tracker_impactentry.value IS 'Numeric value of the environmental impact';
COMMENT ON COLUMN tracker_impactentry.description IS 'Optional user description of the entry';
COMMENT ON COLUMN tracker_impactentry.created_at IS 'Timestamp when entry was created (auto-set)';

-- ============================================================================
-- Django Migration Tracking Tables (if needed)
-- ============================================================================
-- These tables are created automatically by Django migrations
-- Only create if you're not using Django migrations

-- CREATE TABLE IF NOT EXISTS django_migrations (
--     id SERIAL PRIMARY KEY,
--     app VARCHAR(255) NOT NULL,
--     name VARCHAR(255) NOT NULL,
--     applied TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
-- );

-- ============================================================================
-- Sample Data (Optional - Comment out in production)
-- ============================================================================
-- Uncomment below to insert test data

/*
-- Create a test user (password is 'testpass123' hashed)
INSERT INTO auth_user (username, email, password, is_active, date_joined)
VALUES (
    'testuser',
    'test@example.com',
    'pbkdf2_sha256$600000$...',  -- Replace with actual Django password hash
    TRUE,
    CURRENT_TIMESTAMP
);

-- Create sample impact entries
INSERT INTO tracker_impactentry (user_id, metric_type, value, description, created_at)
VALUES 
    (1, 'carbon', 5.2, 'Drove to work', CURRENT_TIMESTAMP),
    (1, 'water', 50.0, 'Daily water usage', CURRENT_TIMESTAMP),
    (1, 'energy', 10.5, 'Home electricity', CURRENT_TIMESTAMP);
*/

-- ============================================================================
-- Useful Queries for Testing
-- ============================================================================

-- View all impact entries with user info
-- SELECT 
--     u.username,
--     u.email,
--     e.metric_type,
--     e.value,
--     e.description,
--     e.created_at
-- FROM tracker_impactentry e
-- JOIN auth_user u ON e.user_id = u.id
-- ORDER BY e.created_at DESC;

-- Count entries by metric type
-- SELECT 
--     metric_type,
--     COUNT(*) as count,
--     SUM(value) as total_value,
--     AVG(value) as avg_value
-- FROM tracker_impactentry
-- GROUP BY metric_type;

-- Get user's total impact by metric
-- SELECT 
--     u.username,
--     e.metric_type,
--     SUM(e.value) as total,
--     COUNT(e.id) as entry_count
-- FROM tracker_impactentry e
-- JOIN auth_user u ON e.user_id = u.id
-- WHERE u.id = 1  -- Replace with actual user ID
-- GROUP BY u.username, e.metric_type;

-- ============================================================================
-- End of Schema
-- ============================================================================

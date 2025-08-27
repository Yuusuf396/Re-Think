-- =====================================================
-- GreenTrack - Climatiqq Database Setup for Supabase
-- =====================================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- 1. USER MANAGEMENT & AUTHENTICATION
-- =====================================================

-- Create custom user profile table (extends Django's built-in User)
CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    date_joined TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster user lookups
CREATE INDEX IF NOT EXISTS idx_user_profiles_username ON user_profiles(username);
CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON user_profiles(email);
CREATE INDEX IF NOT EXISTS idx_user_profiles_active ON user_profiles(is_active);

-- =====================================================
-- 2. ENVIRONMENTAL IMPACT TRACKING
-- =====================================================

-- Create metric types enum
CREATE TYPE metric_type_enum AS ENUM ('carbon', 'water', 'energy', 'digital');

-- Create impact entries table
CREATE TABLE IF NOT EXISTS impact_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    metric_type metric_type_enum NOT NULL,
    value DECIMAL(10, 4) NOT NULL CHECK (value >= 0),
    description VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Add constraints for data validation
    CONSTRAINT valid_carbon_value CHECK (
        (metric_type = 'carbon' AND value <= 1000) OR 
        (metric_type != 'carbon')
    ),
    CONSTRAINT valid_water_value CHECK (
        (metric_type = 'water' AND value <= 10000) OR 
        (metric_type != 'water')
    ),
    CONSTRAINT valid_energy_value CHECK (
        (metric_type = 'energy' AND value <= 500) OR 
        (metric_type != 'energy')
    ),
    CONSTRAINT valid_digital_value CHECK (
        (metric_type = 'digital' AND value <= 100) OR 
        (metric_type != 'digital')
    )
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_impact_entries_user_id ON impact_entries(user_id);
CREATE INDEX IF NOT EXISTS idx_impact_entries_metric_type ON impact_entries(metric_type);
CREATE INDEX IF NOT EXISTS idx_impact_entries_created_at ON impact_entries(created_at);
CREATE INDEX IF NOT EXISTS idx_impact_entries_user_metric ON impact_entries(user_id, metric_type);
CREATE INDEX IF NOT EXISTS idx_impact_entries_user_date ON impact_entries(user_id, created_at);

-- =====================================================
-- 3. AI SUGGESTIONS & RECOMMENDATIONS
-- =====================================================

-- Create AI suggestions table
CREATE TABLE IF NOT EXISTS ai_suggestions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    suggestion_type VARCHAR(50) NOT NULL, -- 'carbon_reduction', 'water_saving', 'energy_efficiency'
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    impact_level VARCHAR(20) CHECK (impact_level IN ('Low', 'Medium', 'High')),
    effort_level VARCHAR(20) CHECK (effort_level IN ('Low', 'Medium', 'High')),
    carbon_savings DECIMAL(10, 4), -- estimated carbon reduction
    ai_model_version VARCHAR(50),
    confidence_score DECIMAL(3, 2) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    is_implemented BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for AI suggestions
CREATE INDEX IF NOT EXISTS idx_ai_suggestions_user_id ON ai_suggestions(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_suggestions_type ON ai_suggestions(suggestion_type);
CREATE INDEX IF NOT EXISTS idx_ai_suggestions_impact ON ai_suggestions(impact_level);
CREATE INDEX IF NOT EXISTS idx_ai_suggestions_created ON ai_suggestions(created_at);

-- =====================================================
-- 4. USER GOALS & TARGETS
-- =====================================================

-- Create user goals table
CREATE TABLE IF NOT EXISTS user_goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    goal_type metric_type_enum NOT NULL,
    target_value DECIMAL(10, 4) NOT NULL,
    current_value DECIMAL(10, 4) DEFAULT 0,
    goal_period VARCHAR(20) CHECK (goal_period IN ('daily', 'weekly', 'monthly', 'yearly')),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_goal_dates CHECK (end_date > start_date),
    CONSTRAINT valid_target_value CHECK (target_value > 0)
);

-- Create indexes for goals
CREATE INDEX IF NOT EXISTS idx_user_goals_user_id ON user_goals(user_id);
CREATE INDEX IF NOT EXISTS idx_user_goals_type ON user_goals(goal_type);
CREATE INDEX IF NOT EXISTS idx_user_goals_active ON user_goals(is_active);

-- =====================================================
-- 5. ENVIRONMENTAL CALCULATORS & FACTORS
-- =====================================================

-- Create carbon footprint factors table
CREATE TABLE IF NOT EXISTS carbon_factors (
    id SERIAL PRIMARY KEY,
    activity_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'transport', 'food', 'energy', 'waste'
    factor_value DECIMAL(10, 6) NOT NULL, -- kg CO2 per unit
    unit VARCHAR(20) NOT NULL, -- 'km', 'kWh', 'kg', 'liter'
    source VARCHAR(200), -- reference source
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert common carbon factors
INSERT INTO carbon_factors (activity_name, category, factor_value, unit, source) VALUES
('Car travel (petrol)', 'transport', 0.170, 'km', 'UK Government GHG Conversion Factors'),
('Car travel (diesel)', 'transport', 0.159, 'km', 'UK Government GHG Conversion Factors'),
('Electricity (grid average)', 'energy', 0.233, 'kWh', 'UK Government GHG Conversion Factors'),
('Natural gas', 'energy', 0.184, 'kWh', 'UK Government GHG Conversion Factors'),
('Beef (per kg)', 'food', 13.3, 'kg', 'Poore & Nemecek 2018'),
('Chicken (per kg)', 'food', 6.9, 'kg', 'Poore & Nemecek 2018'),
('Waste to landfill', 'waste', 0.5, 'kg', 'UK Government GHG Conversion Factors');

-- =====================================================
-- 6. USER ACHIEVEMENTS & BADGES
-- =====================================================

-- Create achievements table
CREATE TABLE IF NOT EXISTS user_achievements (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    achievement_type VARCHAR(50) NOT NULL, -- 'carbon_savings', 'streak', 'goal_completion'
    title VARCHAR(100) NOT NULL,
    description TEXT,
    icon_name VARCHAR(50),
    points INTEGER DEFAULT 0,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for achievements
CREATE INDEX IF NOT EXISTS idx_user_achievements_user_id ON user_achievements(user_id);
CREATE INDEX IF NOT EXISTS idx_user_achievements_type ON user_achievements(achievement_type);

-- =====================================================
-- 7. DATA VALIDATION & TRIGGERS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_user_profiles_updated_at 
    BEFORE UPDATE ON user_profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_impact_entries_updated_at 
    BEFORE UPDATE ON impact_entries 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_goals_updated_at 
    BEFORE UPDATE ON user_goals 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_carbon_factors_updated_at 
    BEFORE UPDATE ON carbon_factors 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 8. VIEWS FOR COMMON QUERIES
-- =====================================================

-- View for user dashboard data
CREATE OR REPLACE VIEW user_dashboard AS
SELECT 
    up.id as user_id,
    up.username,
    up.email,
    COUNT(ie.id) as total_entries,
    SUM(CASE WHEN ie.metric_type = 'carbon' THEN ie.value ELSE 0 END) as total_carbon,
    SUM(CASE WHEN ie.metric_type = 'water' THEN ie.value ELSE 0 END) as total_water,
    SUM(CASE WHEN ie.metric_type = 'energy' THEN ie.value ELSE 0 END) as total_energy,
    SUM(CASE WHEN ie.metric_type = 'digital' THEN ie.value ELSE 0 END) as total_digital,
    MAX(ie.created_at) as last_entry_date,
    COUNT(CASE WHEN ie.created_at >= NOW() - INTERVAL '30 days' THEN 1 END) as recent_entries
FROM user_profiles up
LEFT JOIN impact_entries ie ON up.id = ie.user_id
GROUP BY up.id, up.username, up.email;

-- View for environmental impact summary
CREATE OR REPLACE VIEW impact_summary AS
SELECT 
    user_id,
    metric_type,
    COUNT(*) as entry_count,
    SUM(value) as total_value,
    AVG(value) as average_value,
    MIN(value) as min_value,
    MAX(value) as max_value,
    MIN(created_at) as first_entry,
    MAX(created_at) as last_entry
FROM impact_entries
GROUP BY user_id, metric_type;

-- =====================================================
-- 9. FUNCTIONS FOR COMMON OPERATIONS
-- =====================================================

-- Function to calculate user's carbon footprint
CREATE OR REPLACE FUNCTION calculate_carbon_footprint(user_id_param INTEGER)
RETURNS DECIMAL(10, 4) AS $$
DECLARE
    total_carbon DECIMAL(10, 4) := 0;
BEGIN
    SELECT COALESCE(SUM(value), 0)
    INTO total_carbon
    FROM impact_entries
    WHERE user_id = user_id_param AND metric_type = 'carbon';
    
    RETURN total_carbon;
END;
$$ LANGUAGE plpgsql;

-- Function to get user's environmental impact trend
CREATE OR REPLACE FUNCTION get_impact_trend(
    user_id_param INTEGER, 
    metric_type_param metric_type_enum, 
    days_back INTEGER DEFAULT 30
)
RETURNS TABLE (
    date DATE,
    total_value DECIMAL(10, 4),
    entry_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        DATE(ie.created_at) as date,
        SUM(ie.value) as total_value,
        COUNT(*) as entry_count
    FROM impact_entries ie
    WHERE ie.user_id = user_id_param 
        AND ie.metric_type = metric_type_param
        AND ie.created_at >= NOW() - INTERVAL '1 day' * days_back
    GROUP BY DATE(ie.created_at)
    ORDER BY date;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 10. ROW LEVEL SECURITY (RLS) SETUP
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE impact_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_suggestions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;

-- Create policies (these will be customized based on your auth system)
-- For now, we'll create basic policies that you can modify

-- User profiles policy
CREATE POLICY "Users can view own profile" ON user_profiles
    FOR SELECT USING (id = current_setting('app.current_user_id')::INTEGER);

CREATE POLICY "Users can update own profile" ON user_profiles
    FOR UPDATE USING (id = current_setting('app.current_user_id')::INTEGER);

-- Impact entries policy
CREATE POLICY "Users can view own entries" ON impact_entries
    FOR SELECT USING (user_id = current_setting('app.current_user_id')::INTEGER);

CREATE POLICY "Users can insert own entries" ON impact_entries
    FOR INSERT WITH CHECK (user_id = current_setting('app.current_user_id')::INTEGER);

CREATE POLICY "Users can update own entries" ON impact_entries
    FOR UPDATE USING (user_id = current_setting('app.current_user_id')::INTEGER);

CREATE POLICY "Users can delete own entries" ON impact_entries
    FOR DELETE USING (user_id = current_setting('app.current_user_id')::INTEGER);

-- =====================================================
-- 11. INITIAL DATA & SAMPLE RECORDS
-- =====================================================

-- Insert sample user profile (for testing)
INSERT INTO user_profiles (user_id, username, email, first_name, last_name) VALUES
(1, 'demo_user', 'demo@climatiqq.com', 'Demo', 'User')
ON CONFLICT (user_id) DO NOTHING;

-- Insert sample impact entries (for testing)
INSERT INTO impact_entries (user_id, metric_type, value, description) VALUES
(1, 'carbon', 25.5, 'Daily commute by car'),
(1, 'energy', 12.3, 'Home electricity usage'),
(1, 'water', 150.0, 'Daily water consumption'),
(1, 'digital', 2.1, 'Streaming and internet usage')
ON CONFLICT DO NOTHING;

-- =====================================================
-- 12. FINAL SETUP & VERIFICATION
-- =====================================================

-- Create a function to verify database setup
CREATE OR REPLACE FUNCTION verify_database_setup()
RETURNS TABLE (
    table_name TEXT,
    record_count BIGINT,
    status TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'user_profiles'::TEXT as table_name,
        COUNT(*) as record_count,
        CASE WHEN COUNT(*) > 0 THEN 'OK' ELSE 'EMPTY' END as status
    FROM user_profiles
    
    UNION ALL
    
    SELECT 
        'impact_entries'::TEXT as table_name,
        COUNT(*) as record_count,
        CASE WHEN COUNT(*) > 0 THEN 'OK' ELSE 'EMPTY' END as status
    FROM impact_entries
    
    UNION ALL
    
    SELECT 
        'carbon_factors'::TEXT as table_name,
        COUNT(*) as record_count,
        CASE WHEN COUNT(*) > 0 THEN 'OK' ELSE 'EMPTY' END as status
    FROM carbon_factors;
END;
$$ LANGUAGE plpgsql;

-- Display setup verification
SELECT * FROM verify_database_setup();

-- =====================================================
-- SETUP COMPLETE! 🎉
-- =====================================================

COMMENT ON DATABASE current_database() IS 'GreenTrack - Climatiqq Environmental Impact Tracking Database';

-- Display final status
SELECT 
    'Database Setup Complete!' as status,
    NOW() as completed_at,
    version() as postgres_version;

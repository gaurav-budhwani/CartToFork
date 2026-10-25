-- =====================================================================================
-- Food Delivery Product Funnel & Retention Analytics: Database Schema Setup
-- Compatible with PostgreSQL, DuckDB, Snowflake, BigQuery, and SQLite
-- =====================================================================================

-- Table 1: Users Table (User Acquisition & Demographic Segmentation)
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(64) PRIMARY KEY,
    signup_timestamp TIMESTAMP NOT NULL,
    signup_date DATE NOT NULL,
    signup_platform VARCHAR(32) NOT NULL,       -- 'iOS', 'Android', 'Web'
    city VARCHAR(64) NOT NULL,                  -- 'New York', 'San Francisco', 'Chicago', 'Austin', 'Seattle'
    customer_segment VARCHAR(64) NOT NULL,      -- 'New User', 'Occasional / Casual', 'Power User / Loyalist', 'Deal Seeker'
    acquisition_channel VARCHAR(64) NOT NULL    -- 'Organic Search', 'Paid Social', 'Referral', 'Performance Ads'
);

-- Table 2: Sessions Table (User App Sessions & Funnel Summary)
CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    session_start TIMESTAMP NOT NULL,
    session_date DATE NOT NULL,
    platform VARCHAR(32) NOT NULL,              -- 'iOS', 'Android', 'Web'
    city VARCHAR(64) NOT NULL,
    device_type VARCHAR(32) NOT NULL,           -- 'Mobile App', 'Desktop Web', 'Mobile Web'
    has_discount_applied BOOLEAN DEFAULT FALSE,
    max_funnel_stage VARCHAR(32) NOT NULL,      -- '1_app_open', '2_discovery', '3_add_to_cart', '4_checkout', '5_order_success'
    session_duration_sec INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Table 3: Clickstream Event Log (Event-Level User Journey)
CREATE TABLE IF NOT EXISTS events (
    event_id VARCHAR(64) PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    user_id VARCHAR(64) NOT NULL,
    event_time TIMESTAMP NOT NULL,
    event_name VARCHAR(64) NOT NULL,            -- 'app_open', 'restaurant_search', 'view_restaurant', 'view_item',
                                                -- 'add_to_cart', 'view_cart', 'initiate_checkout', 'apply_promo_code',
                                                -- 'payment_attempt', 'order_success', 'order_failure'
    funnel_step VARCHAR(32) NOT NULL,           -- '1_app_open', '2_discovery', '3_add_to_cart', '4_checkout', '5_order_success'
    restaurant_id VARCHAR(64),
    cuisine VARCHAR(64),
    cart_subtotal NUMERIC(10, 2),
    delivery_fee NUMERIC(10, 2),
    service_fee NUMERIC(10, 2),
    discount_amount NUMERIC(10, 2),
    estimated_delivery_minutes INTEGER,
    surge_pricing_active BOOLEAN DEFAULT FALSE,
    failure_reason VARCHAR(128),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Table 4: Orders Table (Transaction & Basket Economics)
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(64) PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    user_id VARCHAR(64) NOT NULL,
    order_timestamp TIMESTAMP NOT NULL,
    order_date DATE NOT NULL,
    order_sequence_number INTEGER NOT NULL,     -- 1 for 1st order, 2 for 2nd order, etc.
    platform VARCHAR(32) NOT NULL,
    city VARCHAR(64) NOT NULL,
    restaurant_id VARCHAR(64) NOT NULL,
    cuisine VARCHAR(64),
    subtotal_amount NUMERIC(10, 2) NOT NULL,
    delivery_fee NUMERIC(10, 2) NOT NULL,
    service_fee NUMERIC(10, 2) NOT NULL,
    discount_amount NUMERIC(10, 2) DEFAULT 0.00,
    total_paid NUMERIC(10, 2) NOT NULL,
    estimated_delivery_minutes INTEGER,
    actual_delivery_minutes INTEGER,
    user_rating INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Indices for analytical query performance
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(session_date);
CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id);
CREATE INDEX IF NOT EXISTS idx_events_user_time ON events(user_id, event_time);
CREATE INDEX IF NOT EXISTS idx_events_name ON events(event_name);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);

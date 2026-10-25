-- =====================================================================================
-- Query 03: Cohort Retention Analysis (D1, D7, D14, D30 Retention)
-- Description: Measures cohort retention for food delivery users. Tracks both:
--              1) App Activity Retention (user opened app / engaged on Day N)
--              2) Order Repurchase Retention (user placed an order on Day N)
--              Includes cohort slices by Acquisition Channel, Platform, and City.
-- =====================================================================================

WITH user_first_touch AS (
    -- Establish user cohort signup week and acquisition attributes
    SELECT 
        u.user_id,
        u.signup_date,
        DATE_TRUNC('week', u.signup_date) AS cohort_week,
        u.signup_platform,
        u.city,
        u.customer_segment,
        u.acquisition_channel
    FROM users u
),

user_daily_activity AS (
    -- Collect all distinct days each user had a session
    SELECT DISTINCT
        user_id,
        session_date AS activity_date
    FROM sessions
),

user_daily_orders AS (
    -- Collect all distinct days each user placed a successful order
    SELECT DISTINCT
        user_id,
        order_date
    FROM orders
),

user_retention_flags AS (
    -- Calculate days elapsed between signup and subsequent activity/orders
    SELECT 
        uft.user_id,
        uft.cohort_week,
        uft.signup_platform,
        uft.city,
        uft.customer_segment,
        uft.acquisition_channel,
        
        -- D1, D7, D14, D30 App Session Retention Flags
        MAX(CASE WHEN uda.activity_date = uft.signup_date + INTERVAL '1 day' THEN 1 ELSE 0 END) AS retained_d1_session,
        MAX(CASE WHEN uda.activity_date BETWEEN uft.signup_date + INTERVAL '6 days' AND uft.signup_date + INTERVAL '7 days' THEN 1 ELSE 0 END) AS retained_d7_session,
        MAX(CASE WHEN uda.activity_date BETWEEN uft.signup_date + INTERVAL '13 days' AND uft.signup_date + INTERVAL '14 days' THEN 1 ELSE 0 END) AS retained_d14_session,
        MAX(CASE WHEN uda.activity_date BETWEEN uft.signup_date + INTERVAL '28 days' AND uft.signup_date + INTERVAL '30 days' THEN 1 ELSE 0 END) AS retained_d30_session,
        
        -- D1, D7, D14, D30 Order Placement Flags
        MAX(CASE WHEN udo.order_date = uft.signup_date + INTERVAL '1 day' THEN 1 ELSE 0 END) AS retained_d1_order,
        MAX(CASE WHEN udo.order_date BETWEEN uft.signup_date + INTERVAL '6 days' AND uft.signup_date + INTERVAL '7 days' THEN 1 ELSE 0 END) AS retained_d7_order,
        MAX(CASE WHEN udo.order_date BETWEEN uft.signup_date + INTERVAL '13 days' AND uft.signup_date + INTERVAL '14 days' THEN 1 ELSE 0 END) AS retained_d14_order,
        MAX(CASE WHEN udo.order_date BETWEEN uft.signup_date + INTERVAL '28 days' AND uft.signup_date + INTERVAL '30 days' THEN 1 ELSE 0 END) AS retained_d30_order
    FROM user_first_touch uft
    LEFT JOIN user_daily_activity uda ON uft.user_id = uda.user_id
    LEFT JOIN user_daily_orders udo ON uft.user_id = udo.user_id
    GROUP BY 
        uft.user_id, 
        uft.cohort_week, 
        uft.signup_platform, 
        uft.city, 
        uft.customer_segment, 
        uft.acquisition_channel,
        uft.signup_date
)

-- -------------------------------------------------------------------------------------
-- Aggregated Cohort Retention Table
-- -------------------------------------------------------------------------------------
SELECT 
    cohort_week,
    signup_platform,
    COUNT(DISTINCT user_id) AS cohort_size,
    
    -- Active Session Retention Rates (%)
    ROUND(100.0 * SUM(retained_d1_session) / COUNT(DISTINCT user_id), 2)  AS d1_session_retention_pct,
    ROUND(100.0 * SUM(retained_d7_session) / COUNT(DISTINCT user_id), 2)  AS d7_session_retention_pct,
    ROUND(100.0 * SUM(retained_d14_session) / COUNT(DISTINCT user_id), 2) AS d14_session_retention_pct,
    ROUND(100.0 * SUM(retained_d30_session) / COUNT(DISTINCT user_id), 2) AS d30_session_retention_pct,
    
    -- Order Placement Retention Rates (%)
    ROUND(100.0 * SUM(retained_d1_order) / COUNT(DISTINCT user_id), 2)    AS d1_order_retention_pct,
    ROUND(100.0 * SUM(retained_d7_order) / COUNT(DISTINCT user_id), 2)    AS d7_order_retention_pct,
    ROUND(100.0 * SUM(retained_d14_order) / COUNT(DISTINCT user_id), 2)   AS d14_order_retention_pct,
    ROUND(100.0 * SUM(retained_d30_order) / COUNT(DISTINCT user_id), 2)   AS d30_order_retention_pct
FROM user_retention_flags
GROUP BY cohort_week, signup_platform
ORDER BY cohort_week DESC, signup_platform ASC;

-- =====================================================================================
-- Query 02: Funnel Segmentation by Platform, City, Customer Segment, and Discount Usage
-- Description: Measures funnel stage drop-offs sliced by strategic dimensions to reveal
--              where friction is concentrated across platforms, cohorts, and geography.
-- =====================================================================================

WITH session_details AS (
    SELECT 
        s.session_id,
        s.user_id,
        s.platform,
        s.city,
        u.customer_segment,
        CASE WHEN s.has_discount_applied THEN 'Discount Applied' ELSE 'No Discount' END AS promo_group,
        
        -- Funnel Stage progression flags
        1 AS s1_app_open,
        MAX(CASE WHEN e.event_name IN ('restaurant_search', 'view_restaurant', 'view_item') THEN 1 ELSE 0 END) AS s2_discovery,
        MAX(CASE WHEN e.event_name IN ('add_to_cart', 'view_cart') THEN 1 ELSE 0 END) AS s3_add_to_cart,
        MAX(CASE WHEN e.event_name IN ('initiate_checkout', 'apply_promo_code') THEN 1 ELSE 0 END) AS s4_checkout,
        MAX(CASE WHEN e.event_name = 'order_success' THEN 1 ELSE 0 END) AS s5_order_success
    FROM sessions s
    JOIN users u ON s.user_id = u.user_id
    LEFT JOIN events e ON s.session_id = e.session_id
    GROUP BY s.session_id, s.user_id, s.platform, s.city, u.customer_segment, s.has_discount_applied
)

-- -------------------------------------------------------------------------------------
-- Part A: Segmentation by Platform (iOS, Android, Web)
-- -------------------------------------------------------------------------------------
SELECT 
    'Platform' AS dimension_type,
    platform AS dimension_value,
    COUNT(DISTINCT session_id) AS total_sessions,
    
    -- Volumes
    SUM(s1_app_open)      AS app_open_vol,
    SUM(s2_discovery)     AS discovery_vol,
    SUM(s3_add_to_cart)   AS add_to_cart_vol,
    SUM(s4_checkout)      AS checkout_vol,
    SUM(s5_order_success) AS order_success_vol,
    
    -- Stage-over-Stage Conversion Rates (%)
    ROUND(100.0 * SUM(s2_discovery) / NULLIF(SUM(s1_app_open), 0), 2) AS open_to_discovery_pct,
    ROUND(100.0 * SUM(s3_add_to_cart) / NULLIF(SUM(s2_discovery), 0), 2) AS discovery_to_cart_pct,
    ROUND(100.0 * SUM(s4_checkout) / NULLIF(SUM(s3_add_to_cart), 0), 2) AS cart_to_checkout_pct,
    ROUND(100.0 * SUM(s5_order_success) / NULLIF(SUM(s4_checkout), 0), 2) AS checkout_to_order_pct,
    
    -- End-to-End Funnel Conversion Rate (%)
    ROUND(100.0 * SUM(s5_order_success) / NULLIF(SUM(s1_app_open), 0), 2) AS end_to_end_conversion_pct
FROM session_details
GROUP BY platform

UNION ALL

-- -------------------------------------------------------------------------------------
-- Part B: Segmentation by Customer Segment
-- -------------------------------------------------------------------------------------
SELECT 
    'Customer Segment' AS dimension_type,
    customer_segment AS dimension_value,
    COUNT(DISTINCT session_id) AS total_sessions,
    
    SUM(s1_app_open),
    SUM(s2_discovery),
    SUM(s3_add_to_cart),
    SUM(s4_checkout),
    SUM(s5_order_success),
    
    ROUND(100.0 * SUM(s2_discovery) / NULLIF(SUM(s1_app_open), 0), 2),
    ROUND(100.0 * SUM(s3_add_to_cart) / NULLIF(SUM(s2_discovery), 0), 2),
    ROUND(100.0 * SUM(s4_checkout) / NULLIF(SUM(s3_add_to_cart), 0), 2),
    ROUND(100.0 * SUM(s5_order_success) / NULLIF(SUM(s4_checkout), 0), 2),
    ROUND(100.0 * SUM(s5_order_success) / NULLIF(SUM(s1_app_open), 0), 2)
FROM session_details
GROUP BY customer_segment

UNION ALL

-- -------------------------------------------------------------------------------------
-- Part C: Segmentation by City
-- -------------------------------------------------------------------------------------
SELECT 
    'City' AS dimension_type,
    city AS dimension_value,
    COUNT(DISTINCT session_id) AS total_sessions,
    
    SUM(s1_app_open),
    SUM(s2_discovery),
    SUM(s3_add_to_cart),
    SUM(s4_checkout),
    SUM(s5_order_success),
    
    ROUND(100.0 * SUM(s2_discovery) / NULLIF(SUM(s1_app_open), 0), 2),
    ROUND(100.0 * SUM(s3_add_to_cart) / NULLIF(SUM(s2_discovery), 0), 2),
    ROUND(100.0 * SUM(s4_checkout) / NULLIF(SUM(s3_add_to_cart), 0), 2),
    ROUND(100.0 * SUM(s5_order_success) / NULLIF(SUM(s4_checkout), 0), 2),
    ROUND(100.0 * SUM(s5_order_success) / NULLIF(SUM(s1_app_open), 0), 2)
FROM session_details
GROUP BY city

UNION ALL

-- -------------------------------------------------------------------------------------
-- Part D: Segmentation by Discount Usage
-- -------------------------------------------------------------------------------------
SELECT 
    'Discount Usage' AS dimension_type,
    promo_group AS dimension_value,
    COUNT(DISTINCT session_id) AS total_sessions,
    
    SUM(s1_app_open),
    SUM(s2_discovery),
    SUM(s3_add_to_cart),
    SUM(s4_checkout),
    SUM(s5_order_success),
    
    ROUND(100.0 * SUM(s2_discovery) / NULLIF(SUM(s1_app_open), 0), 2),
    ROUND(100.0 * SUM(s3_add_to_cart) / NULLIF(SUM(s2_discovery), 0), 2),
    ROUND(100.0 * SUM(s4_checkout) / NULLIF(SUM(s3_add_to_cart), 0), 2),
    ROUND(100.0 * SUM(s5_order_success) / NULLIF(SUM(s4_checkout), 0), 2),
    ROUND(100.0 * SUM(s5_order_success) / NULLIF(SUM(s1_app_open), 0), 2)
FROM session_details
GROUP BY promo_group

ORDER BY dimension_type, end_to_end_conversion_pct DESC;

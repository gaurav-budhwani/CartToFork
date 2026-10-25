-- =====================================================================================
-- Query 05: Drop-off Deep Dive & Root-Cause Diagnostic Analytics
-- Objective: Investigate the #1 drop-off in the funnel (Cart-to-Order Abandonment).
-- Hypotheses Tested:
--   1. Fee Burden Elasticity: Does a high ratio of (Delivery Fee + Service Fee) / Subtotal drive checkout churn?
--   2. ETA Sensitivity: At what delivery time threshold (minutes) do users abandon their carts?
--   3. Basket Size Economics: Do sub-$20 carts abandon at higher rates due to minimum order friction?
--   4. Technical / Payment Failures: Does gateway latency or technical failure explain checkout drops?
-- =====================================================================================

WITH checkout_sessions AS (
    -- Analyze all sessions that initiated checkout review
    SELECT 
        s.session_id,
        s.user_id,
        s.platform,
        s.city,
        u.customer_segment,
        s.has_discount_applied,
        
        -- Checkout economics from events
        MAX(e.cart_subtotal) AS subtotal,
        MAX(e.delivery_fee)  AS delivery_fee,
        MAX(e.service_fee)   AS service_fee,
        MAX(COALESCE(e.delivery_fee, 0) + COALESCE(e.service_fee, 0)) AS total_fees,
        MAX(e.estimated_delivery_minutes) AS eta_minutes,
        MAX(CASE WHEN e.surge_pricing_active THEN 1 ELSE 0 END) AS surge_active,
        
        -- Order success flag
        MAX(CASE WHEN e.event_name = 'order_success' THEN 1 ELSE 0 END) AS is_order_success,
        MAX(e.failure_reason) AS failure_reason
    FROM sessions s
    JOIN users u ON s.user_id = u.user_id
    JOIN events e ON s.session_id = e.session_id
    WHERE s.max_funnel_stage IN ('4_checkout', '5_order_success')
    GROUP BY s.session_id, s.user_id, s.platform, s.city, u.customer_segment, s.has_discount_applied
),

enriched_metrics AS (
    SELECT 
        *,
        -- Fee Burden Ratio: Percentage of subtotal taken by fees
        ROUND(100.0 * total_fees / NULLIF(subtotal, 0), 1) AS fee_burden_ratio_pct,
        
        -- Categorical Fee Burden Buckets
        CASE 
            WHEN (100.0 * total_fees / NULLIF(subtotal, 0)) < 15.0 THEN '1. Low Fee (< 15% of cart)'
            WHEN (100.0 * total_fees / NULLIF(subtotal, 0)) BETWEEN 15.0 AND 25.0 THEN '2. Moderate Fee (15% - 25%)'
            WHEN (100.0 * total_fees / NULLIF(subtotal, 0)) BETWEEN 25.01 AND 35.0 THEN '3. High Fee (25% - 35%)'
            ELSE '4. Extreme Fee Shock (> 35%)'
        END AS fee_burden_bracket,
        
        -- ETA Buckets
        CASE 
            WHEN eta_minutes < 25 THEN '1. Fast (< 25 mins)'
            WHEN eta_minutes BETWEEN 25 AND 39 THEN '2. Standard (25 - 39 mins)'
            WHEN eta_minutes BETWEEN 40 AND 54 THEN '3. Delayed (40 - 54 mins)'
            ELSE '4. Critical Delay (55+ mins)'
        END AS eta_bracket,
        
        -- Basket Subtotal Buckets
        CASE 
            WHEN subtotal < 15.0 THEN '1. Micro Basket (< $15)'
            WHEN subtotal BETWEEN 15.0 AND 24.99 THEN '2. Small Basket ($15 - $24.99)'
            WHEN subtotal BETWEEN 25.0 AND 39.99 THEN '3. Medium Basket ($25 - $39.99)'
            ELSE '4. Large Basket ($40+)'
        END AS basket_bracket
    FROM checkout_sessions
)

-- -------------------------------------------------------------------------------------
-- Diagnostic Diagnostic 1: Checkout Conversion Rate by Fee Burden Ratio
-- -------------------------------------------------------------------------------------
SELECT 
    'Fee Burden Bracket' AS diagnostic_dimension,
    fee_burden_bracket AS bracket,
    COUNT(session_id) AS checkout_sessions_count,
    SUM(is_order_success) AS orders_placed,
    COUNT(session_id) - SUM(is_order_success) AS abandoned_checkouts,
    ROUND(100.0 * SUM(is_order_success) / COUNT(session_id), 2) AS checkout_to_order_conversion_pct,
    ROUND(100.0 * (1.0 - SUM(is_order_success) * 1.0 / COUNT(session_id)), 2) AS checkout_abandonment_pct,
    ROUND(AVG(subtotal), 2) AS avg_subtotal,
    ROUND(AVG(total_fees), 2) AS avg_fees
FROM enriched_metrics
GROUP BY fee_burden_bracket

UNION ALL

-- -------------------------------------------------------------------------------------
-- Diagnostic Diagnostic 2: Checkout Conversion Rate by Estimated Delivery Time (ETA)
-- -------------------------------------------------------------------------------------
SELECT 
    'ETA Bracket' AS diagnostic_dimension,
    eta_bracket AS bracket,
    COUNT(session_id) AS checkout_sessions_count,
    SUM(is_order_success) AS orders_placed,
    COUNT(session_id) - SUM(is_order_success) AS abandoned_checkouts,
    ROUND(100.0 * SUM(is_order_success) / COUNT(session_id), 2) AS checkout_to_order_conversion_pct,
    ROUND(100.0 * (1.0 - SUM(is_order_success) * 1.0 / COUNT(session_id)), 2) AS checkout_abandonment_pct,
    ROUND(AVG(subtotal), 2) AS avg_subtotal,
    ROUND(AVG(total_fees), 2) AS avg_fees
FROM enriched_metrics
GROUP BY eta_bracket

UNION ALL

-- -------------------------------------------------------------------------------------
-- Diagnostic Diagnostic 3: Checkout Conversion Rate by Basket Size Bucket
-- -------------------------------------------------------------------------------------
SELECT 
    'Basket Subtotal Bracket' AS diagnostic_dimension,
    basket_bracket AS bracket,
    COUNT(session_id) AS checkout_sessions_count,
    SUM(is_order_success) AS orders_placed,
    COUNT(session_id) - SUM(is_order_success) AS abandoned_checkouts,
    ROUND(100.0 * SUM(is_order_success) / COUNT(session_id), 2) AS checkout_to_order_conversion_pct,
    ROUND(100.0 * (1.0 - SUM(is_order_success) * 1.0 / COUNT(session_id)), 2) AS checkout_abandonment_pct,
    ROUND(AVG(subtotal), 2) AS avg_subtotal,
    ROUND(AVG(total_fees), 2) AS avg_fees
FROM enriched_metrics
GROUP BY basket_bracket

ORDER BY diagnostic_dimension, bracket ASC;

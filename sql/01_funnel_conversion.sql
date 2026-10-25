-- =====================================================================================
-- Query 01: Food Delivery Product Funnel Conversion & Drop-off Analysis
-- Description: Measures stage-over-stage and cumulative conversion from
--              App Open -> Restaurant Discovery -> Add to Cart -> Checkout -> Successful Order.
-- =====================================================================================

WITH session_funnel_flags AS (
    -- Identify which milestone stages each session reached
    SELECT 
        s.session_id,
        s.user_id,
        s.platform,
        s.city,
        s.session_date,
        -- Stage 1: App Open (always 1 for any session logged)
        1 AS reached_app_open,
        
        -- Stage 2: Restaurant Discovery (browsed feed, searched, or viewed restaurant menu)
        MAX(CASE WHEN e.event_name IN ('restaurant_search', 'view_restaurant', 'view_item') THEN 1 ELSE 0 END) AS reached_discovery,
        
        -- Stage 3: Add to Cart (added at least 1 dish/item to cart)
        MAX(CASE WHEN e.event_name IN ('add_to_cart', 'view_cart') THEN 1 ELSE 0 END) AS reached_add_to_cart,
        
        -- Stage 4: Checkout Start (navigated to checkout review / payment screen)
        MAX(CASE WHEN e.event_name IN ('initiate_checkout', 'apply_promo_code') THEN 1 ELSE 0 END) AS reached_checkout,
        
        -- Stage 5: Order Success (transaction approved and order created)
        MAX(CASE WHEN e.event_name = 'order_success' THEN 1 ELSE 0 END) AS reached_order_success
    FROM sessions s
    LEFT JOIN events e ON s.session_id = e.session_id
    GROUP BY s.session_id, s.user_id, s.platform, s.city, s.session_date
),

stage_counts AS (
    -- Aggregate total volume reaching each stage
    SELECT 
        COUNT(DISTINCT session_id) AS total_sessions,
        SUM(reached_app_open)      AS stage_1_app_open,
        SUM(reached_discovery)     AS stage_2_discovery,
        SUM(reached_add_to_cart)   AS stage_3_add_to_cart,
        SUM(reached_checkout)      AS stage_4_checkout,
        SUM(reached_order_success) AS stage_5_order_success
    FROM session_funnel_flags
),

unpivoted_funnel AS (
    -- Structure into clean stage rows for reporting & BI visualizations
    SELECT 
        1 AS step_order, 
        '1. App Open' AS funnel_stage, 
        stage_1_app_open AS sessions_reached,
        total_sessions AS baseline_sessions
    FROM stage_counts
    UNION ALL
    SELECT 
        2 AS step_order, 
        '2. Restaurant Discovery' AS funnel_stage, 
        stage_2_discovery AS sessions_reached,
        total_sessions AS baseline_sessions
    FROM stage_counts
    UNION ALL
    SELECT 
        3 AS step_order, 
        '3. Add to Cart' AS funnel_stage, 
        stage_3_add_to_cart AS sessions_reached,
        total_sessions AS baseline_sessions
    FROM stage_counts
    UNION ALL
    SELECT 
        4 AS step_order, 
        '4. Initiate Checkout' AS funnel_stage, 
        stage_4_checkout AS sessions_reached,
        total_sessions AS baseline_sessions
    FROM stage_counts
    UNION ALL
    SELECT 
        5 AS step_order, 
        '5. Successful Order' AS funnel_stage, 
        stage_5_order_success AS sessions_reached,
        total_sessions AS baseline_sessions
    FROM stage_counts
)

SELECT 
    step_order,
    funnel_stage,
    sessions_reached,
    LAG(sessions_reached, 1) OVER (ORDER BY step_order) AS previous_stage_sessions,
    
    -- Absolute drop-off from previous step
    COALESCE(LAG(sessions_reached, 1) OVER (ORDER BY step_order) - sessions_reached, 0) AS drop_off_volume,
    
    -- Step-over-step conversion rate (% of users advancing from the previous step)
    ROUND(
        100.0 * sessions_reached / NULLIF(LAG(sessions_reached, 1) OVER (ORDER BY step_order), 0), 
        2
    ) AS step_conversion_rate_pct,
    
    -- Step-over-step drop-off rate (% of users abandoning at this transition)
    ROUND(
        100.0 * (1.0 - (sessions_reached * 1.0 / NULLIF(LAG(sessions_reached, 1) OVER (ORDER BY step_order), 0))), 
        2
    ) AS step_dropoff_rate_pct,
    
    -- Cumulative conversion rate from initial App Open
    ROUND(
        100.0 * sessions_reached / NULLIF(baseline_sessions, 0), 
        2
    ) AS cumulative_conversion_rate_pct
FROM unpivoted_funnel
ORDER BY step_order ASC;

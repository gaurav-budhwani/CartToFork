-- =====================================================================================
-- Query 04: Repeat-Order Rate & Re-order Velocity Analysis
-- Description: Measures 30-day repeat order conversion, distribution of order frequency
--              (1 order vs 2+ orders), days between 1st and 2nd orders, and the critical
--              impact of First-Order Discount Usage on long-term repeat behavior.
-- =====================================================================================

WITH user_order_sequencing AS (
    -- Sequence all orders chronologically per user
    SELECT 
        o.order_id,
        o.user_id,
        o.order_timestamp,
        o.order_date,
        o.platform,
        o.city,
        o.discount_amount,
        o.subtotal_amount,
        ROW_NUMBER() OVER (PARTITION BY o.user_id ORDER BY o.order_timestamp ASC) AS user_order_seq,
        LEAD(o.order_timestamp, 1) OVER (PARTITION BY o.user_id ORDER BY o.order_timestamp ASC) AS next_order_timestamp
    FROM orders o
),

first_order_profile AS (
    -- Extract attributes of each user's maiden order
    SELECT 
        user_id,
        order_timestamp AS first_order_time,
        order_date AS first_order_date,
        platform AS first_order_platform,
        city AS first_order_city,
        subtotal_amount AS first_order_subtotal,
        discount_amount AS first_order_discount,
        CASE WHEN discount_amount > 0 THEN 'Used Promo on 1st Order' ELSE 'No Promo on 1st Order' END AS first_order_discount_type,
        next_order_timestamp,
        -- Days between 1st and 2nd order
        ROUND(
            CAST(EXTRACT(EPOCH FROM (next_order_timestamp - order_timestamp)) / 86400.0 AS NUMERIC), 
            1
        ) AS days_to_second_order
    FROM user_order_sequencing
    WHERE user_order_seq = 1
),

user_lifetime_stats AS (
    -- Aggregate total lifetime orders per user
    SELECT 
        u.user_id,
        u.customer_segment,
        u.signup_platform,
        u.city,
        fop.first_order_discount_type,
        fop.days_to_second_order,
        COUNT(o.order_id) AS total_orders,
        SUM(COALESCE(o.total_paid, 0)) AS total_spend,
        CASE 
            WHEN COUNT(o.order_id) = 0 THEN '0 Orders (No conversion)'
            WHEN COUNT(o.order_id) = 1 THEN '1 Order (One-and-done churn)'
            WHEN COUNT(o.order_id) = 2 THEN '2 Orders (First repeat)'
            WHEN COUNT(o.order_id) BETWEEN 3 AND 5 THEN '3-5 Orders (Active)'
            ELSE '6+ Orders (Power User)'
        END AS order_frequency_bracket,
        CASE WHEN COUNT(o.order_id) >= 2 THEN 1 ELSE 0 END AS is_repeat_buyer
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.user_id
    LEFT JOIN first_order_profile fop ON u.user_id = fop.user_id
    GROUP BY 
        u.user_id, 
        u.customer_segment, 
        u.signup_platform, 
        u.city, 
        fop.first_order_discount_type, 
        fop.days_to_second_order
)

-- -------------------------------------------------------------------------------------
-- Part A: Repeat Purchase Rate & Velocity by First Order Discount Behavior
-- -------------------------------------------------------------------------------------
SELECT 
    COALESCE(first_order_discount_type, 'All Transacting Users') AS promo_cohort,
    COUNT(DISTINCT user_id) AS total_buyers,
    SUM(is_repeat_buyer) AS repeat_buyers_count,
    
    -- Repeat Order Rate (% of 1st-time buyers who place a 2nd order)
    ROUND(100.0 * SUM(is_repeat_buyer) / NULLIF(COUNT(DISTINCT user_id), 0), 2) AS repeat_order_rate_pct,
    
    -- Re-order Velocity (Avg Days to 2nd Order)
    ROUND(AVG(days_to_second_order), 1) AS avg_days_to_second_order,
    
    -- Average Lifetime Orders & Spend
    ROUND(AVG(total_orders), 2) AS avg_lifetime_orders,
    ROUND(AVG(total_spend), 2) AS avg_lifetime_spend
FROM user_lifetime_stats
WHERE total_orders >= 1
GROUP BY first_order_discount_type

UNION ALL

-- -------------------------------------------------------------------------------------
-- Part B: Repeat Purchase Rate by Customer Segment
-- -------------------------------------------------------------------------------------
SELECT 
    customer_segment AS promo_cohort,
    COUNT(DISTINCT user_id) AS total_buyers,
    SUM(is_repeat_buyer) AS repeat_buyers_count,
    ROUND(100.0 * SUM(is_repeat_buyer) / NULLIF(COUNT(DISTINCT user_id), 0), 2) AS repeat_order_rate_pct,
    ROUND(AVG(days_to_second_order), 1) AS avg_days_to_second_order,
    ROUND(AVG(total_orders), 2) AS avg_lifetime_orders,
    ROUND(AVG(total_spend), 2) AS avg_lifetime_spend
FROM user_lifetime_stats
WHERE total_orders >= 1
GROUP BY customer_segment

ORDER BY promo_cohort;

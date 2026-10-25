# Power BI DAX Measures Library
## Production-Grade DAX Formulas for Food Delivery Funnel & Retention Analytics

Copy and paste these measures directly into your Power BI Desktop model.

---

### 1. Base Volume & Financial Measures

```dax
// Total Sessions
Total Sessions = 
DISTINCTCOUNT(fact_sessions[session_id])

// Total Registered Users
Total Users = 
DISTINCTCOUNT(dim_users[user_id])

// Total Successful Orders
Total Orders = 
DISTINCTCOUNT(fact_orders[order_id])

// Total Food Subtotal ($)
Total Subtotal Amount = 
SUM(fact_orders[subtotal_amount])

// Total Fees Incurred ($)
Total Fees Incurred = 
SUM(fact_orders[delivery_fee]) + SUM(fact_orders[service_fee])

// Total Gross Merchandise Value (GMV / Total Paid)
Total Revenue GMV = 
SUM(fact_orders[total_paid])

// Average Order Value (AOV)
Average Order Value = 
DIVIDE([Total Subtotal Amount], [Total Orders], 0)

// Fee Burden Ratio (%)
Fee Burden Ratio Pct = 
DIVIDE([Total Fees Incurred], [Total Subtotal Amount], 0) * 100
```

---

### 2. Funnel Stage Milestone Measures

```dax
// Stage 1: App Open Volume
Funnel S1 App Open = 
CALCULATE(
    [Total Sessions],
    fact_sessions[max_funnel_stage] IN {
        "1_app_open", "2_discovery", "3_add_to_cart", "4_checkout", "5_order_success"
    }
)

// Stage 2: Restaurant Discovery Volume
Funnel S2 Discovery = 
CALCULATE(
    [Total Sessions],
    fact_sessions[max_funnel_stage] IN {
        "2_discovery", "3_add_to_cart", "4_checkout", "5_order_success"
    }
)

// Stage 3: Add to Cart Volume
Funnel S3 Add To Cart = 
CALCULATE(
    [Total Sessions],
    fact_sessions[max_funnel_stage] IN {
        "3_add_to_cart", "4_checkout", "5_order_success"
    }
)

// Stage 4: Checkout Start Volume
Funnel S4 Initiate Checkout = 
CALCULATE(
    [Total Sessions],
    fact_sessions[max_funnel_stage] IN {
        "4_checkout", "5_order_success"
    }
)

// Stage 5: Successful Order Volume
Funnel S5 Order Success = 
CALCULATE(
    [Total Sessions],
    fact_sessions[max_funnel_stage] = "5_order_success"
)
```

---

### 3. Funnel Conversion & Drop-off Rates

```dax
// Overall End-to-End Funnel Conversion Rate
Overall Funnel Conversion Rate = 
DIVIDE([Funnel S5 Order Success], [Funnel S1 App Open], 0) * 100

// Stage 1 -> 2 Conversion (Open to Discovery)
Conv S1 to S2 Pct = 
DIVIDE([Funnel S2 Discovery], [Funnel S1 App Open], 0) * 100

// Stage 2 -> 3 Conversion (Discovery to Add to Cart)
Conv S2 to S3 Pct = 
DIVIDE([Funnel S3 Add To Cart], [Funnel S2 Discovery], 0) * 100

// Stage 3 -> 4 Conversion (Add to Cart to Checkout)
Conv S3 to S4 Pct = 
DIVIDE([Funnel S4 Initiate Checkout], [Funnel S3 Add To Cart], 0) * 100

// Stage 4 -> 5 Conversion (Checkout to Order Success)
Conv S4 to S5 Pct = 
DIVIDE([Funnel S5 Order Success], [Funnel S4 Initiate Checkout], 0) * 100

// Checkout Drop-off Rate (The #1 Friction Stage)
Checkout Dropoff Rate Pct = 
(1 - DIVIDE([Funnel S5 Order Success], [Funnel S4 Initiate Checkout], 0)) * 100

// Absolute Checkout Abandonment Volume
Checkout Abandoned Volume = 
[Funnel S4 Initiate Checkout] - [Funnel S5 Order Success]
```

---

### 4. Cohort Retention & Repeat Purchase Measures

```dax
// Day 1 App Retention Rate (%)
D1 App Retention Rate Pct = 
VAR CohortUsers = DISTINCTCOUNT(dim_users[user_id])
VAR RetainedUsers = 
    CALCULATE(
        DISTINCTCOUNT(fact_sessions[user_id]),
        FILTER(
            fact_sessions,
            RELATED(dim_users[signup_date]) + 1 = fact_sessions[session_date]
        )
    )
RETURN
DIVIDE(RetainedUsers, CohortUsers, 0) * 100

// Day 7 App Retention Rate (%)
D7 App Retention Rate Pct = 
VAR CohortUsers = DISTINCTCOUNT(dim_users[user_id])
VAR RetainedUsers = 
    CALCULATE(
        DISTINCTCOUNT(fact_sessions[user_id]),
        FILTER(
            fact_sessions,
            fact_sessions[session_date] >= RELATED(dim_users[signup_date]) + 6 &&
            fact_sessions[session_date] <= RELATED(dim_users[signup_date]) + 7
        )
    )
RETURN
DIVIDE(RetainedUsers, CohortUsers, 0) * 100

// Day 30 App Retention Rate (%)
D30 App Retention Rate Pct = 
VAR CohortUsers = DISTINCTCOUNT(dim_users[user_id])
VAR RetainedUsers = 
    CALCULATE(
        DISTINCTCOUNT(fact_sessions[user_id]),
        FILTER(
            fact_sessions,
            fact_sessions[session_date] >= RELATED(dim_users[signup_date]) + 28 &&
            fact_sessions[session_date] <= RELATED(dim_users[signup_date]) + 30
        )
    )
RETURN
DIVIDE(RetainedUsers, CohortUsers, 0) * 100

// 30-Day Repeat Order Rate (%)
Repeat Order Rate 30D Pct = 
VAR FirstTimeBuyers = 
    CALCULATE(
        DISTINCTCOUNT(fact_orders[user_id]),
        fact_orders[order_sequence_number] = 1
    )
VAR RepeatBuyers = 
    CALCULATE(
        DISTINCTCOUNT(fact_orders[user_id]),
        fact_orders[order_sequence_number] >= 2
    )
RETURN
DIVIDE(RepeatBuyers, FirstTimeBuyers, 0) * 100
```

# Data Model & Star Schema Architecture
## Tableau & Power BI Data Architecture Specification

### 1. Conceptual & Logical Data Model
This architecture follows the Kimball Dimensional Modeling methodology for event-driven clickstream analytics, structured into a high-performance **Star / Constellation Schema**.

```mermaid
erDiagram
    DIM_USERS ||--o{ FACT_SESSIONS : "initiates (1:N)"
    DIM_USERS ||--o{ FACT_ORDERS : "places (1:N)"
    DIM_DATE ||--o{ FACT_SESSIONS : "session_date (1:N)"
    DIM_DATE ||--o{ FACT_ORDERS : "order_date (1:N)"
    FACT_SESSIONS ||--o{ FACT_EVENTS : "generates (1:N)"
    FACT_SESSIONS ||--o{ FACT_ORDERS : "converts_to (1:0..1)"

    DIM_USERS {
        string user_id PK
        timestamp signup_timestamp
        date signup_date
        string signup_platform
        string city
        string customer_segment
        string acquisition_channel
    }

    DIM_DATE {
        date calendar_date PK
        int year
        string quarter
        string month_name
        int month_num
        int week_of_year
        string day_name
        boolean is_weekend
    }

    FACT_SESSIONS {
        string session_id PK
        string user_id FK
        timestamp session_start
        date session_date FK
        string platform
        string city
        string device_type
        boolean has_discount_applied
        string max_funnel_stage
        int session_duration_sec
    }

    FACT_EVENTS {
        string event_id PK
        string session_id FK
        string user_id FK
        timestamp event_time
        string event_name
        string funnel_step
        string restaurant_id
        string cuisine
        numeric cart_subtotal
        numeric delivery_fee
        numeric service_fee
        numeric discount_amount
        int estimated_delivery_minutes
        boolean surge_pricing_active
        string failure_reason
    }

    FACT_ORDERS {
        string order_id PK
        string session_id FK
        string user_id FK
        timestamp order_timestamp
        date order_date FK
        int order_sequence_number
        string platform
        string city
        string restaurant_id
        string cuisine
        numeric subtotal_amount
        numeric delivery_fee
        numeric service_fee
        numeric discount_amount
        numeric total_paid
        int estimated_delivery_minutes
        int actual_delivery_minutes
        int user_rating
    }
```

---

### 2. Table Relationships & Cardinality Table

| Relationship | From Table (Column) | To Table (Column) | Cardinality | Cross-Filter Direction | Role in Analytics |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **User Cohort to Sessions** | `dim_users.user_id` | `fact_sessions.user_id` | 1 to Many (`1:*`) | Single (`dim_users` filters `fact_sessions`) | Slices funnel conversion by acquisition channel & persona |
| **User Cohort to Orders** | `dim_users.user_id` | `fact_orders.user_id` | 1 to Many (`1:*`) | Single (`dim_users` filters `fact_orders`) | Cohort retention (D1/D7/D30) & LTV repeat tracking |
| **Calendar to Sessions** | `dim_date.calendar_date` | `fact_sessions.session_date`| 1 to Many (`1:*`) | Single (`dim_date` filters `fact_sessions`) | Time intelligence (MoM, WoW trend analysis) |
| **Calendar to Orders** | `dim_date.calendar_date` | `fact_orders.order_date` | 1 to Many (`1:*`) | Single (`dim_date` filters `fact_orders`) | Sales and transaction velocity tracking |
| **Session to Events** | `fact_sessions.session_id` | `fact_events.session_id` | 1 to Many (`1:*`) | Single (`fact_sessions` filters `fact_events`) | Micro-conversion drop-off analysis |
| **Session to Orders** | `fact_sessions.session_id` | `fact_orders.session_id` | 1 to 1 (or 0..1) | Both Directions | Bridges session funnel context with realized transaction margins |

---

### 3. Optimization Guidelines
1. **Granularity Alignment**:
   - `fact_sessions` contains **one row per app session**, representing the primary denominator for top-of-funnel conversion.
   - `fact_events` contains **one row per user interaction telemetry**, used specifically for deep-dive diagnostics (fee sensitivity, item browsing, payment attempts).
   - In Power BI and Tableau, avoid joining `fact_events` to `fact_orders` directly. Always traverse through `dim_users` or `fact_sessions` to prevent fan-out / Cartesian multiplication of dollar metrics.
2. **Aggregated Summary Tables (Marts)**:
   - For ultra-fast interactive dashboards, pre-aggregate `funnel_summary.csv` and `cohort_retention.csv` to ensure sub-50ms dashboard response times.

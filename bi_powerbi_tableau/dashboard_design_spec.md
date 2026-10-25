# Dashboard Design Specification
## Food Delivery Product Funnel & Retention Analytics (Tableau & Power BI)

---

### 1. Visual Layout Hierarchy & Grid Architecture

The dashboard is structured into a clean, data-dense layout optimized for standard executive reporting:

```
+----------------------------------------------------------------------------------------------------------+
|  HEADER: Food Delivery Funnel & Retention Analytics | Platform | City | Segment | Discount Usage         |
+----------------------------------------------------------------------------------------------------------+
|  ROW 1: KPI BANNER                                                                                       |
|  [ Total Sessions ]   [ End-to-End Conv % ]   [ Critical Bottleneck ]   [ Total Orders ] [ D30 Retention]|
|      41,176                10.20%               Checkout: 70.63% Drop        4,200             45.83%    |
+--------------------------------------------------------------------+-------------------------------------+
|  ROW 2: FUNNEL PROGRESSION                                         | ROW 2: COHORT RETENTION             |
|                                                                    |                                     |
|  [ Funnel Step-over-Step Progression ]                             | [ Monthly Cohort Retention Table ]  |
|   1. App Open           (100.0%) - 41,176 sessions                 |   Cohorts vs D1, D7, D14, D30       |
|   2. Discovery           (78.8%) - 32,426 sessions                 |                                     |
|   3. Add to Cart         (59.8%) - 19,381 sessions                 | [ Re-order Velocity Chart ]         |
|   4. Initiate Checkout   (73.8%) - 14,298 sessions                 |   Organic 1st Order: 38.90 days     |
|   5. Successful Order    (29.4%) -  4,200 orders                   |   Promo 1st Order:   43.95 days     |
+--------------------------------------------------------------------+-------------------------------------+
|  ROW 3: ROOT-CAUSE DIAGNOSTIC SUITE                                                                      |
|  [ Delivery ETA Sensitivity Curve ]            [ Checkout Failure Categorization ]                       |
|  Abandonment Rate vs Promised Delivery Mins    ETA Delays (31.6%), Fee Surcharges (25.7%), Timeouts      |
+----------------------------------------------------------------------------------------------------------+
|  ROW 4: PROPOSED PRODUCT INTERVENTION & A/B CALCULATOR                                                   |
|  Feature: Project Clarity (Upfront Menu Pricing + In-Cart Free Delivery Milestone + Flexible Pacing)    |
|  Model: Target Lift Slider (+3.5%) -> Incremental Orders: +501/mo | Projected Annual GMV: +₹3,486,960    |
+----------------------------------------------------------------------------------------------------------+
```

---

### 2. Design Tokens & Color Palette (Clean Minimalist Light Theme)

| Token Name | Hex Code | Purpose |
| :--- | :--- | :--- |
| **Canvas Background** | `#FFFFFF` | Clean white primary background |
| **Surface / Card Background** | `#FFFFFF` / `#F9FAFB` | Crisp, clean panels with subtle gray borders |
| **Borders** | `#E5E7EB` / `#D1D5DB` | 1px clean separator lines (no heavy shadows) |
| **Primary Text** | `#111827` | Deep charcoal / black for maximum legibility |
| **Secondary Text** | `#4B5563` | Neutral gray for descriptions and sub-labels |
| **Muted Metadata** | `#6B7280` | Subtle captions and axis labels |
| **Functional Red (Drop-off / Alert)** | `#DC2626` | Bottleneck callouts and abandonment metrics |
| **Functional Green (Success)** | `#16A34A` | Successful conversions and positive retention |
| **Functional Navy / Slate** | `#1E293B` / `#334155` | Primary bar and line charts |

---

### 3. Visualizations Configuration

#### Visual 1: Step-over-Step Funnel Chart
- **Visual Type**: Horizontal or Stepped Bar Chart.
- **Color**: Neutral Slate `#1E293B` for progression, with Stage 4 (Checkout) highlighted in subtle Red `#DC2626` to signal the **70.63% drop-off bottleneck**.
- **Data Labels**: Session volume and step-over-step conversion rate.

#### Visual 2: Delivery ETA Sensitivity Curve
- **Visual Type**: Line Chart with markers.
- **Metric 1 (Green `#16A34A`)**: Checkout-to-Order Conversion Rate.
- **Metric 2 (Dashed Red `#DC2626`)**: Checkout Abandonment Rate.
- **Key Observation**: Conversion plummets from 100% when delivery is under 25 minutes down to 14.2% when delivery exceeds 55 minutes.

#### Visual 3: Cohort Retention Table
- **Visual Type**: Clean data table.
- **Columns**: Signup Cohort, Cohort Size, Day 1, Day 7, Day 14, Day 30.
- **Formatting**: Simple percentage readouts with subtle borders.

#### Visual 4: Re-order Velocity Comparison
- **Visual Type**: Grouped Bar Chart comparing Organic First Orders vs Promo First Orders.
- **Observation**: Organic buyers re-order 5.05 days faster (38.90 days) than coupon-subsidized buyers (43.95 days).

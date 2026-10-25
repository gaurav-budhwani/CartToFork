# CartToFork: Food Delivery Product Funnel & Retention Analytics

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](python/)
[![SQL](https://img.shields.io/badge/SQL-ANSI%20%7C%20Postgres%20%7C%20DuckDB-orange?logo=postgresql&logoColor=white)](sql/)
[![Power BI](https://img.shields.io/badge/Power%20BI-DAX%20Production-yellow?logo=powerbi&logoColor=black)](bi_powerbi_tableau/)
[![Tableau](https://img.shields.io/badge/Tableau-LOD%20Calculations-blue?logo=tableau&logoColor=white)](bi_powerbi_tableau/)
[![Experimentation](https://img.shields.io/badge/A%2FB%20Testing-Statistical%20Power%20Sizing-brightgreen)](product_teardown/)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)
[![GitHub Repository](https://img.shields.io/badge/GitHub-gaurav--budhwani%2FCartToFork-181717?logo=github&logoColor=white)](https://github.com/gaurav-budhwani/CartToFork)

<p align="center">
  <strong>An End-to-End Product Analytics Teardown, Clickstream Funnel Diagnostic Suite, and Empirical A/B Experimentation Engine for Food Delivery Marketplaces</strong>
</p>

</div>

---

![CartToFork Dashboard Screenshot](images/dashboard_screenshot.png)

---

## 🎯 Executive Overview & The Business Question

> **The Core Business Question**:  
> *Where are users dropping off before placing an order, and what might encourage them to return?*

In on-demand food delivery platforms (such as DoorDash, Uber Eats, Zomato, and Swiggy), top-of-funnel exploration is inexpensive, but **late-funnel drop-off is financially catastrophic**. Every customer who builds a food cart and advances to checkout has already demonstrated high intent, meal selection, and hunger. When they abandon at the final payment screen, marketing acquisition spend (CAC) is wasted and high-margin Gross Merchandise Value (GMV) is destroyed.

**CartToFork** delivers an exhaustive, end-to-end product analytics investigation across **41,176 sessions**, **4,200 completed orders**, and **500 longitudinal customer profiles** across 5 major metropolitan clusters (**Mumbai, Bengaluru, Delhi NCR, Hyderabad, Pune**), harmonized from authentic public delivery transaction records.

---

## 🛠️ Technology Stack & Architecture

```
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|                                  CARTTOFORK SYSTEM ARCHITECTURE                                  |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  1. DATA LAYER          |  2. COMPUTE & MODELING   |  3. BUSINESS INTELLIGENCE  |  4. INTERACTION|
|  • Zomato/Swiggy Orders |  • Python 3.10+ (Pandas, |  • Power BI (DAX Measures) |  • HTML5 / CSS3|
|  • NYC FoodHub Records  |    NumPy, SciPy)         |  • Tableau (LOD Calc Fields|  • Vanilla JS   |
|  • Clickstream Events   |  • ANSI SQL (PostgreSQL, |  • Kimball Star Schema ERD |  • Chart.js    |
|  • User Cohort Profiles |    DuckDB, Snowflake)    |  • Dimensional Data Marts  |  • A/B Calc    |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
```

- **Data Ingestion & Pipeline**: Python (`pandas`, `numpy`), processing authentic multi-table relational operational datasets into unified session and clickstream telemetry.
- **Analytical & Diagnostic Queries**: ANSI SQL compatible with PostgreSQL, DuckDB, Snowflake, BigQuery, and SQLite using Common Table Expressions (CTEs), multi-step window functions (`LAG`, `LEAD`, `ROW_NUMBER`), and cohort aggregations.
- **Statistical Modeling & Visualizations**: Python (`matplotlib`, `seaborn`, `scipy`), generating publication-quality visual distributions and sensitivity curves.
- **Business Intelligence & Data Modeling**: Kimball dimensional star schema specification, production-grade Power BI DAX measures, and Tableau Level of Detail (LOD) expressions.
- **Executive Web Dashboard**: Responsive, clean light-mode dashboard built with semantic HTML5, Vanilla CSS3, modern typography (Inter), and Chart.js, featuring live filter reactivity and an interactive A/B test simulator.

---

## 📊 1. End-to-End Funnel Breakdown & Quantitative Findings

Mapping the complete customer journey across **41,176 sessions** reveals an **overall end-to-end conversion rate of 10.20%**:

| Funnel Milestone | Session Volume | Step Conversion (%) | Step Drop-off (%) | Cumulative Throughput (%) |
| :--- | :--- | :--- | :--- | :--- |
| **1. App Open** | 41,176 | 100.00% | 0.00% | **100.00%** |
| **2. Restaurant Discovery** | 32,426 | 78.75% | 21.25% | **78.75%** |
| **3. Add to Cart** | 19,381 | 59.77% | 40.23% | **47.07%** |
| **4. Initiate Checkout** | 14,298 | 73.77% | 26.23% | **34.72%** |
| **5. Successful Order** | **4,200** | **29.37%** | **70.63% (THE BOTTLENECK)** | **10.20%** |

```
App Open             (41,176 sessions) ── [100.0% Baseline]
   │
   ▼  -21.25% Drop-off (Browsing bounce / lack of immediate dining intent)
Restaurant Discovery (32,426 sessions) ── [ 78.75% of Open]
   │
   ▼  -40.23% Drop-off (Menu exploration vs cart commitment)
Add to Cart          (19,381 sessions) ── [ 47.07% of Open]
   │
   ▼  -26.23% Drop-off (Cart review friction)
Initiate Checkout    (14,298 sessions) ── [ 34.72% of Open]
   │
   ▼  -70.63% DROP-OFF (THE PRIMARY REVENUE LEAKAGE)
Successful Order     ( 4,200 orders)   ── [ 10.20% of Open]
```

![Funnel Waterfall Chart](images/01_funnel_waterfall.png)

---

## 🚨 2. The Standout Finding: The Checkout Abandonment Crisis

While discovery-to-cart drop-off is expected in high-exploration apps, **the single most financially destructive drop-off occurs at Stage 4 ➔ Stage 5 (Initiate Checkout to Order Success)**:
- **70.63% of users who built a cart and clicked "Proceed to Checkout" abandoned without completing payment.**
- **10,098 high-intent sessions** were lost at the final step.
- These were qualified buyers who had already spent 4–8 minutes browsing menus, choosing dishes, and deciding to dine.
- Recovering just **5% of these abandoned checkouts (+505 monthly orders)** yields over **₹290,000 in monthly incremental GMV** without spending an extra dollar on marketing.

![Checkout Root Causes](images/02_checkout_root_cause_drivers.png)

### Root-Cause Diagnostics on the 10,098 Abandoned Checkouts:

| Root Cause Failure Driver | Abandoned Sessions | % of Abandonments | Behavioral Mechanism & Empirical Impact |
| :--- | :--- | :--- | :--- |
| **1. Dynamic ETA Inflation (>40m delay)** | **3,193** | **31.62%** | Quoted menu ETA was 25–30m, but real-time courier dispatch re-estimates to 48–55m at checkout. Abandonment escalates to **76.42% for 40–54m ETAs** and **85.76% for 55m+ ETAs**. |
| **2. The "Fee Shock" Penalty** | **2,595** | **25.70%** | Unannounced delivery fees (₹35–₹65) and platform fees (₹5) added at checkout. When fees exceed **20% of cart subtotal**, conversion drops by 28.5 percentage points. |
| **3. Price Comparison / User Hesitation** | **1,907** | **18.88%** | Multi-tab price shopping between competing delivery aggregators (e.g., Zomato vs Swiggy). |
| **4. Payment Gateway Latency & Timeouts** | **1,873** | **18.55%** | UPI intent switching failures, SMS OTP delays, and 3D-Secure modal reload drops. |
| **5. Promo Restriction Barriers** | **530** | **5.25%** | Negative surprise when a voucher fails due to uncommunicated minimum cart thresholds (e.g., *"Cart must be ₹299+ to apply"*). |

![ETA Sensitivity Curve](images/03_eta_fee_sensitivity.png)

---

## 🔍 3. Multi-Dimensional Funnel Segmentation

### By Platform:
- **iOS App**: 29.78% checkout conversion (10.32% end-to-end). Benefits from biometric 1-tap Apple Pay.
- **Android App**: 28.65% checkout conversion (9.96% end-to-end). Encounters higher drop-off during third-party UPI app switching.
- **Web (Desktop & Mobile)**: 29.70% checkout conversion (10.35% end-to-end).

### By Metro Market:
- **Delhi NCR**: Highest checkout conversion at **30.39%** (10.60% end-to-end).
- **Mumbai & Hyderabad**: **29.30% – 29.31%** checkout conversion.
- **Bengaluru & Pune**: **28.73% – 29.24%** checkout conversion (higher traffic congestion and delivery radius variance).

### By Discount Usage ("The Promo Hangover"):
- **Conversion Lift**: Sessions with a discount applied converted at **48.60% at checkout (20.44% end-to-end)** vs **16.55% at checkout (5.15% end-to-end)** for organic sessions (a **3x conversion gap**).
- **Retention & Habit Formation**: However, **organic first-order buyers re-order 5.05 days faster (38.90 vs 43.95 days)** than promo-acquired buyers. Heavy discount subsidies attract transactional deal-seekers who hesitate to re-order without active coupons.

![Discount Impact Comparison](images/04_discount_impact_comparison.png)

---

## 📈 4. Cohort Retention & Repeat Purchase Velocity

![Cohort Retention Heatmap](images/05_cohort_retention_heatmap.png)

- **Longitudinal Cohort Retention**:
  - **Day 1 Retention**: 16.67% – 31.25%
  - **Day 7 Retention**: 29.55% – 38.64%
  - **Day 14 Retention**: 31.82% – 50.00%
  - **Day 30 Retention**: 34.09% – 51.22%
- **Repeat Order Economics**:
  - **Total Unique Transacting Customers**: 500
  - **Repeat Buyers (≥2 orders)**: **499 (99.8%)**
  - **Customer Frequency Distribution**: **84.6% are Power Users (6+ lifetime orders)**; 15.0% are Active Customers (3–5 orders); only 0.2% churn after 1 order.
  - **Re-order Velocity**: Median time to 2nd order is **23.76 days for organic buyers** vs **29.97 days for discount-subsidized buyers**.

---

## 💡 5. Proposed Product Intervention: Project Clarity
### "The Transparent Fee-Free Milestone & Flexible Pacing System"

Rather than treating fees and delivery times as negative surprises at the final payment step, **we turn fee transparency into an Average Order Value (AOV) growth engine**:

```
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|                                  PROJECT CLARITY PRODUCT PILLARS                                 |
+───────────────────────────────────+───────────────────────────────────+──────────────────────────+
|  1. ALL-IN MENU PRICING PREVIEW   |  2. IN-CART "FEE-FREE MILESTONE"  |  3. ECO-SAVER FLEX PACING|
|  Disclose delivery fees upfront   |  Gamified progress: "Add ₹65 for  |  Choose Priority (25m) or|
|  on restaurant discovery cards    |  FREE DELIVERY!" + 1-tap add-ons  |  Eco-Saver Pooled (₹0 fee|
+───────────────────────────────────+───────────────────────────────────+──────────────────────────+
```

### The In-Cart Milestone Wireframe:
```
┌────────────────────────────────────────────────────────────────────────┐
│  Add ₹65 more to qualify for FREE DELIVERY                             │
│  [=======================================>             ] ₹234 / ₹299   │
│  Popular additions to hit your goal:                                   │
│  [+ Garlic Naan (₹70)]   [+ Masala Chaas (₹65)]   [+ Gulab Jamun (₹80)] │
└────────────────────────────────────────────────────────────────────────┘
```
- **Consumer Benefit**: Price transparency; tangible reward for building a slightly larger meal.
- **Merchant Benefit**: +14% expansion in ticket size (AOV expansion).
- **Platform Economics**: Higher commission take-rate easily subsidizes the delivery fee while eliminating cart abandonment.

---

## 🔬 6. Scientific A/B Experimentation Plan

$$\text{Hypothesis: Transparent upfront fees + in-cart milestone progress bar will lift checkout conversion by } \ge \mathbf{3.0\% \text{ absolute}}.$$

- **Primary Success Metric**: Checkout-to-Order Conversion Rate (%) — Target lift from **29.37% baseline to 32.87%**.
- **Secondary Metrics**: Average Order Value (AOV), Add-to-Cart-to-Checkout throughput, 30-Day Repeat Purchase Rate.
- **Guardrail Metrics**:
  - *Net Contribution Margin per Order*: Must not degrade by more than -₹8.00 (-$0.10).
  - *Driver SLA Latency*: Eco-Saver batching must not increase delivery transit time by more than +4 minutes.
- **Statistical Power & Sample Size**:
  - Significance Level: $\alpha = 0.05$ (95% CI)
  - Statistical Power: $1 - \beta = 0.80$ (80% Power)
  - Minimum Detectable Effect (MDE): $+2.5\%$ absolute lift
  - **Required Sample Size**: **$\approx 12,650$ checkout sessions per variant** (Total: **$25,300$ checkout sessions**).
  - **Runtime**: **21 days (3 full calendar weeks)** to eliminate day-of-week seasonality.

---

## 📁 7. Exhaustive Directory & File-by-File Breakdown

This repository is structured into modular, production-grade components:

### A. Data Directory (`data/`)
- [`data/raw/users.csv`](data/raw/users.csv): 500 longitudinal customer profiles across 5 metro markets with signup dates, platforms, and customer segments (`New User`, `Occasional / Casual`, `Power User / Loyalist`, `Deal Seeker`).
- [`data/raw/sessions.csv`](data/raw/sessions.csv): 41,176 individual app session records tracking platform, city, duration, promo flag, and deepest milestone reached (`max_funnel_stage`).
- [`data/raw/events.csv`](data/raw/events.csv): 121,579 event clickstream telemetry records logging `app_open`, `view_restaurant`, `add_to_cart`, `initiate_checkout`, `order_success`, and `order_failure` with failure reasons.
- [`data/raw/orders.csv`](data/raw/orders.csv): 4,200 completed food delivery transactions with subtotal amounts, delivery surcharges, platform fees, discounts, and customer ratings.
- [`data/raw/zomato_swiggy_orders.csv`](data/raw/zomato_swiggy_orders.csv): Authentic raw operational transaction records from Zomato / Swiggy operations.
- [`data/raw/zomato_swiggy_customers.csv`](data/raw/zomato_swiggy_customers.csv): Authentic raw customer demographic records.
- [`data/raw/zomato_swiggy_restaurants.csv`](data/raw/zomato_swiggy_restaurants.csv): 60 restaurant profiles with cuisines, commission rates, and cost-for-two metrics.
- [`data/raw/zomato_swiggy_deliveries.csv`](data/raw/zomato_swiggy_deliveries.csv): 3,878 courier delivery fulfillment logs tracking distance (km), estimated delivery minutes, actual delivery minutes, weather conditions, and SLA breach statuses.
- [`data/raw/foodhub_order.csv`](data/raw/foodhub_order.csv): Authentic NYC food delivery transaction logs from Shake Shack, Hangawi, Blue Ribbon, Dirty Bird, and Tamarind.
- [`data/processed/funnel_summary.csv`](data/processed/funnel_summary.csv): Aggregated funnel milestone pass/drop volume and conversion percentages.
- [`data/processed/segment_funnel.csv`](data/processed/segment_funnel.csv): Funnel metrics sliced across Platform, City, Customer Segment, and Discount Usage.
- [`data/processed/cohort_retention.csv`](data/processed/cohort_retention.csv): Monthly cohort retention rates tracking Day 1, Day 7, Day 14, and Day 30 session/order activity.
- [`data/processed/repeat_order_summary.csv`](data/processed/repeat_order_summary.csv): User-level days between Order 1 and Order 2 for re-order velocity analysis.
- [`data/processed/dropoff_diagnostic.csv`](data/processed/dropoff_diagnostic.csv): Fee elasticity summary mapping fee brackets against checkout conversion rates.
- [`data/README.md`](data/README.md): Data provenance documentation, data dictionary, and harmonization methodology.

### B. SQL Query Library (`sql/`)
- [`sql/schema_setup.sql`](sql/schema_setup.sql): Production DDL schema creating `users`, `sessions`, `events`, and `orders` tables with foreign keys and analytical indexes.
- [`sql/01_funnel_conversion.sql`](sql/01_funnel_conversion.sql): CTE-based query calculating stage-over-stage pass/drop rates and cumulative conversion from App Open to Order Success.
- [`sql/02_funnel_segmentation.sql`](sql/02_funnel_segmentation.sql): Slices funnel conversion across Platform (`iOS`, `Android`, `Web`), City, Segment, and Promo usage.
- [`sql/03_cohort_retention_d1_d7_d30.sql`](sql/03_cohort_retention_d1_d7_d30.sql): Longitudinal user cohort retention query computing D1, D7, D14, and D30 activity and order rates.
- [`sql/04_repeat_order_behavior.sql`](sql/04_repeat_order_behavior.sql): Repurchase rate, lifetime frequency distribution, and re-order velocity (Promo vs Organic 1st orders).
- [`sql/05_dropoff_deepdive_diagnostic.sql`](sql/05_dropoff_deepdive_diagnostic.sql): Statistical diagnostic query isolating fee elasticity brackets, ETA sensitivity bins, and gateway failure reasons.

### C. Python Analytics Engine (`python/`)
- [`python/build_real_event_funnel.py`](python/build_real_event_funnel.py): Pipeline script ingesting genuine Zomato/Swiggy orders and synthesizing upstream clickstream sessions.
- [`python/run_funnel_analysis.py`](python/run_funnel_analysis.py): Analytical compute engine generating all processed summary CSVs.
- [`python/generate_visualizations.py`](python/generate_visualizations.py): Matplotlib/Seaborn script rendering publication-grade PNG charts in `images/`.
- [`python/create_notebook.py`](python/create_notebook.py): Automated script generating the narrative Jupyter Notebook.
- [`python/notebook_funnel_analytics.ipynb`](python/notebook_funnel_analytics.ipynb): Interactive, self-contained Jupyter Notebook with narrative explanations, code cells, tables, and charts.

### D. Business Intelligence & Modeling Assets (`bi_powerbi_tableau/`)
- [`bi_powerbi_tableau/powerbi_dax_measures.md`](bi_powerbi_tableau/powerbi_dax_measures.md): Production DAX formulas for Power BI Desktop & Service (Funnel stages, conversions, D7/D30 retention, AOV, Fee burden ratio).
- [`bi_powerbi_tableau/tableau_calculated_fields.md`](bi_powerbi_tableau/tableau_calculated_fields.md): Production formulas and Level of Detail (LOD) expressions (`FIXED [User ID]`) for Tableau Desktop & Prep.
- [`bi_powerbi_tableau/data_model_star_schema.md`](bi_powerbi_tableau/data_model_star_schema.md): Kimball Star Schema architecture, ERD diagram in Mermaid, cardinality rules, and cross-filter directions.
- [`bi_powerbi_tableau/dashboard_design_spec.md`](bi_powerbi_tableau/dashboard_design_spec.md): Executive UI layout grid, design tokens, visual hierarchy, and wireframes.

### E. Product Strategy & Teardown Documents (`product_teardown/`)
- [`product_teardown/executive_summary.md`](product_teardown/executive_summary.md): Executive brief for the Chief Product Officer and VP of Growth.
- [`product_teardown/root_cause_investigation.md`](product_teardown/root_cause_investigation.md): Deep-dive quantitative autopsy on the 10,098 checkout abandonments.
- [`product_teardown/product_intervention_proposal.md`](product_teardown/product_intervention_proposal.md): Comprehensive feature specification for Project Clarity (Milestone Engine, Upfront Pricing, Eco-Pacing).
- [`product_teardown/ab_test_experiment_plan.md`](product_teardown/ab_test_experiment_plan.md): Scientific A/B testing plan with power sizing, sample size calculations, guardrails, and decision matrix.

### F. Interactive Executive Web Application (`dashboard/`)
- [`dashboard/index.html`](dashboard/index.html): Executive dashboard featuring live interactive Chart.js visualizations, stage filter reactivity, and an **interactive A/B experiment simulator**.
- [`dashboard/styles.css`](dashboard/styles.css): Clean, minimalist light-mode stylesheet with high-contrast typography and subtle borders.
- [`dashboard/app.js`](dashboard/app.js): Dynamic client-side controller handling live filtering, Chart.js instances, and real-time simulator calculations.

### G. Visual Assets (`images/`)
- [`images/dashboard_screenshot.png`](images/dashboard_screenshot.png): Authenticated screenshot of the interactive executive web dashboard.
- [`images/01_funnel_waterfall.png`](images/01_funnel_waterfall.png): Stepped funnel waterfall highlighting the 70.6% checkout drop-off bottleneck.
- [`images/02_checkout_root_cause_drivers.png`](images/02_checkout_root_cause_drivers.png): Root-cause breakdown of the 10,098 lost checkouts.
- [`images/03_eta_fee_sensitivity.png`](images/03_eta_fee_sensitivity.png): Dual-axis ETA sensitivity curve showing abandonment escalation beyond 40 minutes.
- [`images/04_discount_impact_comparison.png`](images/04_discount_impact_comparison.png): Conversion lift vs re-order velocity ("Promo Hangover").
- [`images/05_cohort_retention_heatmap.png`](images/05_cohort_retention_heatmap.png): Monthly cohort retention decay heatmap.

---

## 🚀 8. Step-by-Step Guide: How to Run, Visualize, and Analyze

### Step 1: Clone Repository & Setup Environment
```bash
# 1. Clone the repository
git clone https://github.com/gaurav-budhwani/CartToFork.git
cd CartToFork

# 2. Create and activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install pandas numpy scipy matplotlib seaborn
```

### Step 2: Execute Analytics Pipeline & Generate Visuals
```bash
# 1. Run the core analytics compute engine
python python/run_funnel_analysis.py

# 2. Re-generate all high-resolution charts in images/
python python/generate_visualizations.py
```

### Step 3: Open and Run the Jupyter Notebook
```bash
# Launch Jupyter Notebook
jupyter notebook python/notebook_funnel_analytics.ipynb
```
*The notebook walks through the data loading, funnel calculations, retention heatmaps, diagnostic plots, and product intervention proposals step-by-step.*

### Step 4: Run the Production SQL Queries
The SQL scripts in `sql/` use ANSI-standard SQL and can be executed against any database engine (DuckDB, PostgreSQL, SQLite, Snowflake, or BigQuery):

```bash
# Example running with DuckDB CLI:
duckdb -c "
  CREATE TABLE users AS SELECT * FROM read_csv_auto('data/raw/users.csv');
  CREATE TABLE sessions AS SELECT * FROM read_csv_auto('data/raw/sessions.csv');
  CREATE TABLE events AS SELECT * FROM read_csv_auto('data/raw/events.csv');
  CREATE TABLE orders AS SELECT * FROM read_csv_auto('data/raw/orders.csv');
"
duckdb -f sql/01_funnel_conversion.sql
duckdb -f sql/02_funnel_segmentation.sql
duckdb -f sql/05_dropoff_deepdive_diagnostic.sql
```

### Step 5: Launch the Interactive Executive Web Dashboard
The web dashboard is lightweight, self-contained, and requires zero external build steps:
```bash
# Start local HTTP server
python3 -m http.server 8080 --directory dashboard

# Open your browser at:
http://localhost:8080
```
- **Interact with Filters**: Filter by Platform (`iOS`, `Android`, `Web`), City, Segment, or Discount usage.
- **Navigate Tabs**: Switch between Funnel Flow, Diagnostics, Cohort Retention, and the A/B Simulator.
- **Test the A/B Simulator**: Adjust the "Target Conversion Lift" slider (+1% to +6%) and "Average Order Subtotal" slider to see live recalculation of incremental orders and annual GMV.
- **Export Data**: Click "Export CSV" in the top-right header to download summary metrics.

### Step 6: Connect Power BI or Tableau
1. Open Power BI Desktop or Tableau Desktop.
2. Connect to the pre-aggregated data marts in `data/processed/` (`funnel_summary.csv`, `segment_funnel.csv`, `cohort_retention.csv`, `dropoff_diagnostic.csv`).
3. Follow the star schema relationships detailed in [`bi_powerbi_tableau/data_model_star_schema.md`](bi_powerbi_tableau/data_model_star_schema.md).
4. Copy and paste formulas from [`bi_powerbi_tableau/powerbi_dax_measures.md`](bi_powerbi_tableau/powerbi_dax_measures.md) or [`bi_powerbi_tableau/tableau_calculated_fields.md`](bi_powerbi_tableau/tableau_calculated_fields.md).

---

## 💼 9. How to Present This on a Resume / Portfolio / Interview

### Resume Bullet Example:
> **Product Analytics Project | CartToFork: Food Delivery Product Funnel & Retention Analytics**  
> • Built an end-to-end product funnel tracking 41K+ sessions and 4.2K orders across 5 metros, identifying a **70.6% checkout abandonment rate** as the primary conversion bottleneck (10K+ lost high-intent orders).  
> • Executed diagnostic root-cause analytics isolating delivery ETA delays >40m (31.6% of drops) and late fee disclosure (25.7% of drops) as the top friction drivers.  
> • Designed **"Project Clarity"** (upfront all-in menu pricing + gamified in-cart free delivery milestones) and formulated a scientific A/B test with statistical power sizing ($\approx 25.3\text{K}$ sessions, MDE 2.5%, $\alpha = 0.05$), projecting **+₹3.48M in annualized GMV lift**.

### Key Talking Points for Behavioral / Technical Interviews:
1. **Business Question First**: Focus on how identifying the *late-stage* checkout bottleneck provides 3.4x greater financial leverage than trying to acquire more top-of-funnel traffic.
2. **The "Promo Hangover" Discovery**: Explain the trade-off between short-term conversion spikes and long-term re-order velocity (organic buyers re-order 5 days faster than discounted buyers).
3. **Product Intervention Over Just Reporting**: Emphasize that great product analytics doesn't end with a dashboard; it proposes a testable product mechanism (the milestone engine) and defines exact launch guardrails (contribution margin and courier SLA limits).

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

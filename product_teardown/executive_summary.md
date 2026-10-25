# Executive Summary: Food Delivery Funnel & Retention Analytics
**Prepared for**: Chief Product Officer, VP of Growth & Product Analytics  
**Objective**: Identify conversion leakage across the ordering lifecycle, diagnose the primary drop-off driver, and outline a high-leverage product intervention with an experimentation roadmap.

---

## 1. High-Level Performance Snapshot

An analysis of **41,176 user sessions** and **4,200 completed orders** across 5 major metropolitan clusters (**Mumbai, Bengaluru, Delhi NCR, Hyderabad, Pune**) reveals an **end-to-end conversion rate of 10.20%** from app open to successful order placement.

```
App Open             (41,176 sessions)  [100.0% Baseline]
   │
   ▼  -21.25% Drop-off (Browsing intent bounce)
Restaurant Discovery (32,426 sessions)  [ 78.75% of Open]
   │
   ▼  -40.23% Drop-off (Menu exploration vs cart intent)
Add to Cart          (19,381 sessions)  [ 47.07% of Open]
   │
   ▼  -26.23% Drop-off (Cart review friction)
Initiate Checkout    (14,298 sessions)  [ 34.72% of Open]
   │
   ▼  -70.63% Drop-off (THE CRITICAL BOTTLENECK)
Successful Order     ( 4,200 orders)    [ 10.20% of Open]
```

---

## 2. The Critical Drop-off: Checkout Abandonment

While top-of-funnel drop-off is expected during restaurant discovery, **the most financially destructive drop-off occurs at Stage 4 ➔ 5 (Initiate Checkout to Order Success):**
- **70.63% of users who deliberately built a food cart and proceeded to checkout abandon without completing payment.**
- **10,098 high-intent sessions** were abandoned at this final step.
- These were qualified buyers who had already spent 4–8 minutes browsing menus, choosing dishes, and deciding to dine.

---

## 3. Why Are Users Abandoning at Checkout?

Diagnostic analysis of the 10,098 abandoned checkout sessions isolated three primary drivers:

1. **Delivery ETA Delays (>40 minutes) - 31.62% of abandonments (3,193 sessions)**:
   Menu cards display standard 25–30 minute estimates. When real-time courier dispatch recalculates to 45–55+ minutes at checkout, abandonment escalates sharply to **76.42% for 40–54m ETAs** and **85.76% for 55m+ ETAs**.
2. **Late Fee Disclosure & Surcharges - 25.70% of abandonments (2,595 sessions)**:
   Delivery fees (₹35–₹65) and platform fees (₹5) are introduced at the final payment review screen. For carts under ₹250, fees inflate the total order cost by **20% to 35%**, triggering price shock.
3. **Price Comparison & User Hesitation - 18.88% (1,907 sessions)**:
   Shoppers comparing final totals across competing platforms (e.g. Zomato vs Swiggy).
4. **Payment Gateway Latency & Timeouts - 18.55% (1,873 sessions)**:
   Involuntary drops driven by third-party UPI intent switching delays and 3D-Secure modal reloads.

---

## 4. Proposed Product Intervention: Project Clarity
To resolve these friction points without relying on standard features that already exist across delivery apps, we propose **"Project Clarity"**:
1. **Predictive Intent-Pipelining**: Trigger soft-alerts to restaurant kitchens and soft-hold nearby couriers during checkout dwell time ($\ge 20$ seconds), shaving 11 minutes off quoted checkout delivery time.
2. **Algorithmic Basket Neutralizer**: An inline 1-tap module directly on the payment card that identifies high-margin companion items that clear free delivery thresholds, demonstrating net-zero marginal cost (e.g. *"Add ₹60 Garlic Naan: Removes ₹50 fee, net cost only +₹10"*).
3. **Cross-App Parity Shield & 10-Minute Surge Freeze**: A 10-minute contractual price freeze coupled with a best-net-price guarantee, eliminating the incentive to switch to competing apps to compare prices.
4. **Failsafe Async Payment Recovery**: A 5-minute background grace period for delayed UPI confirmations that keeps orders queued rather than dropping carts on timeout.

---

## 5. Expected Business Impact & Experiment Plan
- **Primary Metric**: Checkout-to-Order Conversion Rate (Target: +3.5% absolute lift from 29.37% baseline to 32.87%).
- **Projected Financial Gain**: +501 incremental orders/month per cohort, generating **+₹3,486,960 in annualized incremental GMV**.
- **A/B Experiment Design**: 21-day randomized controlled trial on 25,300 checkout sessions (50/50 split) with strict guardrails on contribution margin per order and delivery SLA variance.

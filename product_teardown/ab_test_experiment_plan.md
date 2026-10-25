# A/B Experimentation Plan: Project Clarity Evaluation
## Practical Measurement Framework for Checkout Optimization

---

### 1. Scientific Hypothesis Statement

$$\text{If we deploy auto-applied best coupons, one-tap in-app UPI payments, and an on-time delivery guarantee,}$$
$$\text{then Checkout-to-Order Conversion Rate will increase by } \ge \mathbf{3.0\% \text{ absolute}},$$
$$\text{because unexpected fees, payment app-switching failures, and delivery delay anxiety are directly eliminated.}$$

---

### 2. Metric Hierarchy & Governance

#### A. Primary Success Metric
- **Checkout-to-Order Conversion Rate (%)**:
  $$\text{Conv}_{\text{Checkout}\to\text{Order}} = \frac{\text{Sessions Reaching 'order\_success'}}{\text{Sessions Reaching 'initiate\_checkout'}} \times 100$$
  - *Baseline*: **29.37%**
  - *Minimum Detectable Effect (MDE)*: **+2.5% to +3.5% absolute lift** (Target: $\ge 32.37\%$)

#### B. Secondary / Diagnostic Metrics
1. **Payment Success Rate (%)**: Measure the increase in completed transactions resulting from one-tap UPI payments (targeting a 50% drop in payment failures).
2. **Average Order Value (AOV)**: Ensure auto-applied coupons do not reduce net ticket sizes below profitable thresholds.
3. **Checkout Completion Time (Seconds)**: Measure how much faster users complete checkout when they do not need to search for promo codes or switch apps.
4. **Day 30 Repeat Order Rate (%)**: Measure whether the on-time delivery guarantee and wallet credits encourage subsequent orders.

#### C. Guardrail Metrics (Zero-Tolerance Boundaries)
1. **Net Contribution Margin per Order (₹)**: Must not decrease by more than **-₹6.00/order** after accounting for discount subsidies.
2. **On-Time Delivery Breach Rate**: Late deliveries triggering the ₹50 wallet compensation must remain below **3.5%** of all fulfilled orders.
3. **Refund / Dispute Rate**: Must remain below **1.0%**.

---

### 3. Experiment Design & Randomization Architecture

```
                                  [ All Active Checkout Sessions ]
                                                 │
                                                 ▼
                            ┌───────────────────────────────────────────┐
                            │  User-Level Hashing (MurmurHash3 on User) │
                            └─────────────────────┬─────────────────────┘
                                                  │
                            ┌─────────────────────┴─────────────────────┐
                            ▼ (50%)                                     ▼ (50%)
                 [ Variant A: Control ]                      [ Variant B: Treatment ]
                 Status Quo Checkout:                        Project Clarity:
                 • Manual coupon search and entry            • Auto-applied best available coupon
                 • Redirect to external UPI apps             • Native 1-tap in-app UPI payment
                 • Standard estimated delivery time          • Guaranteed on-time delivery or ₹50 credit
```

- **Randomization Unit**: **`user_id`** (Persistent across sessions and devices).
- **Stratification Factors**: Stratified by **Platform** (`iOS`, `Android`, `Web`) and **Metro Market** (`Delhi NCR`, `Mumbai`, `Bengaluru`, `Hyderabad`, `Pune`) to prevent demographic skew.

---

### 4. Sample Size & Statistical Power Calculation

Using standard two-tailed hypothesis testing for proportions:
- **Baseline Conversion Rate ($p_1$)**: $29.37\%$ ($0.2937$)
- **Expected Lift / MDE ($\delta$)**: $+2.5\%$ absolute ($p_2 = 0.3187$)
- **Significance Level ($\alpha$)**: $0.05$ ($95\%$ Confidence Interval, $Z_{\alpha/2} = 1.96$)
- **Statistical Power ($1 - \beta$)**: $0.80$ ($80\%$ Power, $Z_{\beta} = 0.8416$)

$$n = \frac{\left( Z_{\alpha/2} \sqrt{2 \cdot \bar{p}(1 - \bar{p})} + Z_\beta \sqrt{p_1(1-p_1) + p_2(1-p_2)} \right)^2}{(p_2 - p_1)^2}$$

Where $\bar{p} = \frac{p_1 + p_2}{2} = 0.3062$.

- **Required Sample Size**: **$\approx 12,650$ checkout sessions per variant** (Total: **$25,300$ checkout sessions**).
- **Traffic Feasibility**: At an average of $\approx 1,200$ checkout sessions per day across target metros:
  - **Required Runtime**: **21 days (3 full calendar weeks)** to account for weekend vs weekday ordering patterns.

---

### 5. Phased Rollout Schedule & Risk Mitigation

```
Week 1 (Days 1–3)   ──> 5% Canary Ramp (Internal staff + Pune metro)
                         Verify 1-tap UPI integration and auto-coupon ranking speed.
Week 1 (Days 4–7)   ──> 20% Ramp (10% Control / 10% Treatment across all cities)
                         Monitor contribution margin and wallet compensation payouts.
Week 2–3 (Days 8–21)──> 100% Experiment Active (50% Control / 50% Treatment)
                         Collect primary sample; evaluate conversion, AOV, and guardrails.
Day 22              ──> Final Executive Decision Review & Production Rollout.
```

---

### 6. Decision Framework

| Outcome Scenario | Primary Metric (Conv %) | Guardrail Metric (Net Margin) | Actionable Decision |
| :--- | :--- | :--- | :--- |
| **Scenario 1: Green Light (Clear Win)** | Statistically significant lift ($\ge +2.5\%$, $p < 0.05$) | Neutral or Positive ($\Delta \ge -₹4.00$) | **Ship 100% to production**. Default auto-coupons and 1-tap UPI across all platforms. |
| **Scenario 2: Conversion Win, Margin Bleed** | Statistically significant lift ($\ge +3.0\%$) | Negative breach ($\Delta < -₹6.00$/order) | **Tune coupon criteria**: Cap maximum auto-applied discount at ₹50. Re-test. |
| **Scenario 3: Flat / Inconclusive** | No significant change ($-1.0\% \le \Delta \le +1.0\%$) | Neutral | **Segment teardown**: Evaluate if UPI users saw high lift while card users showed no difference. |
| **Scenario 4: Negative Breach** | Conversion drops ($p < 0.05$) | Any | **Immediate rollback**. Investigate payment gateway error rates. |

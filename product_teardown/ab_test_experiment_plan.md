# A/B Experimentation Plan: Project Clarity Evaluation
## Rigorous Measurement Framework for Predictive Intent-Pipelining & Basket Neutralization

---

### 1. Scientific Hypothesis Statement

$$\text{If we deploy predictive intent-pipelining (reducing checkout ETA by 11m), an algorithmic 1-tap basket neutralizer, and a cross-app price freeze,}$$
$$\text{then Checkout-to-Order Conversion Rate will increase by } \ge \mathbf{3.0\% \text{ absolute}},$$
$$\text{because the primary drivers of late-stage drop-off (ETA inflation, fee penalties, price comparison, and payment timeouts) are systematically eliminated.}$$

---

### 2. Metric Hierarchy & Governance

#### A. Primary Success Metric
- **Checkout-to-Order Conversion Rate (%)**:
  $$\text{Conv}_{\text{Checkout}\to\text{Order}} = \frac{\text{Sessions Reaching 'order\_success'}}{\text{Sessions Reaching 'initiate\_checkout'}} \times 100$$
  - *Baseline*: **29.37%**
  - *Minimum Detectable Effect (MDE)*: **+2.5% to +3.5% absolute lift** (Target: $\ge 32.37\%$)

#### B. Secondary / Diagnostic Metrics
1. **Average Order Value (AOV)**: Track whether the 1-tap Basket Neutralizer expands cart sizes by converting delivery fees into high-margin food items. (Target: +6% to +10% lift).
2. **Checkout Dwell Time (Seconds)**: Measure whether the 90-second kitchen slot reservation incentive and 10-minute price freeze reduce hesitation and shorten checkout time.
3. **Cart Abandonment Rate (%)**: Measure drop-off reduction on the final payment review screen.
4. **Day 30 Repeat Order Rate (%)**: Measure whether faster delivery times and transparent pricing build long-term retention.

#### C. Guardrail Metrics (Zero-Tolerance Boundaries)
1. **Net Contribution Margin per Order (₹)**: Must NOT degrade by more than **-₹8.00/order** due to subsidized fee neutralization. (The incremental food margin and platform take-rate must offset fee waivers).
2. **Merchant Food Waste / Preparation Cancellation Rate**: Must remain below **0.5%** to confirm that the soft-lock pre-alert does not cause premature cooking of unconfirmed meals.
3. **Courier Restaurant Dwell Time**: Must decrease or remain flat (Max allowable courier wait: $\le 4.5$ minutes at merchant).

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
                 Status Quo Checkout:                        Project Clarity Engine:
                 • Sequential post-pay dispatch              • Predictive Intent-Pipelining (ETA -11m)
                 • Static delivery fees added at end         • 1-Tap Algorithmic Basket Neutralizer
                 • Variable surge pricing active             • 10-Min Price Freeze & Parity Shield
                 • Instant failure on UPI timeout            • 5-Min Background Async UPI Recovery
```

- **Randomization Unit**: **`user_id`** (Persistent across sessions and devices).  
  *Rationale*: Session-level randomization would cause cognitive dissonance if a user sees a price freeze and pre-warm incentive in the afternoon and a static fee banner in the evening.
- **Stratification Factors**: Stratified by **Platform** (`iOS`, `Android`, `Web`) and **Metro Market** (`Delhi NCR`, `Mumbai`, `Bengaluru`, `Hyderabad`, `Pune`) to prevent demographic skew.

---

### 4. Sample Size & Statistical Power Calculation

Using two-tailed hypothesis testing for proportions:
- **Baseline Conversion Rate ($p_1$)**: $29.37\%$ ($0.2937$)
- **Expected Lift / MDE ($\delta$)**: $+2.5\%$ absolute ($p_2 = 0.3187$)
- **Significance Level ($\alpha$)**: $0.05$ ($95\%$ Confidence Interval, $Z_{\alpha/2} = 1.96$)
- **Statistical Power ($1 - \beta$)**: $0.80$ ($80\%$ Power, $Z_{\beta} = 0.8416$)

$$n = \frac{\left( Z_{\alpha/2} \sqrt{2 \cdot \bar{p}(1 - \bar{p})} + Z_\beta \sqrt{p_1(1-p_1) + p_2(1-p_2)} \right)^2}{(p_2 - p_1)^2}$$

Where $\bar{p} = \frac{p_1 + p_2}{2} = 0.3062$.

- **Required Sample Size**: **$\approx 12,650$ checkout sessions per variant** (Total: **$25,300$ checkout sessions**).
- **Traffic Feasibility**: At an average of $\approx 1,200$ checkout sessions per day across target metros:
  - **Required Runtime**: **21 days (3 full calendar weeks)** to capture weekend vs weekday ordering cycles and eliminate day-of-week bias.

---

### 5. Phased Rollout Schedule & Risk Mitigation

```
Week 1 (Days 1–3)   ──> 5% Canary Ramp (Internal staff + Pune metro)
                         Verify KDS soft-alert integration and payment gateway hooks.
Week 1 (Days 4–7)   ──> 20% Ramp (10% Control / 10% Treatment across all cities)
                         Health check on contribution margin, courier dwell, and food waste.
Week 2–3 (Days 8–21)──> 100% Experiment Active (50% Control / 50% Treatment)
                         Collect primary sample; evaluate conversion, AOV, and guardrails.
Day 22              ──> Final Executive Decision Review & Gradual 100% Rollout.
```

---

### 6. Decision Framework

| Outcome Scenario | Primary Metric (Conv %) | Guardrail Metric (Net Margin) | Actionable Decision |
| :--- | :--- | :--- | :--- |
| **Scenario 1: Green Light (Clear Win)** | Statistically significant lift ($\ge +2.5\%$, $p < 0.05$) | Neutral or Positive ($\Delta \ge -₹5.00$) | **Ship 100% to production**. Expand KDS soft-alerts to all restaurant partners. |
| **Scenario 2: Conversion Win, Margin Bleed** | Statistically significant lift ($\ge +3.0\%$) | Negative breach ($\Delta < -₹8.00$/order) | **Tune neutralizer algorithm**: Require higher minimum margin item pairings. Re-test. |
| **Scenario 3: Flat / Inconclusive** | No significant change ($-1.0\% \le \Delta \le +1.0\%$) | Neutral | **Segment teardown**: Evaluate if intent-pipelining worked in dense clusters but lacked couriers in suburbs. |
| **Scenario 4: Negative Breach** | Conversion drops ($p < 0.05$) | Any | **Immediate rollback**. Conduct qualitative user research on checkout countdown timers. |

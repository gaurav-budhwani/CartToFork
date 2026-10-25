# A/B Experimentation Plan: Project Clarity Evaluation
## Rigorous Measurement Framework for the Fee-Free Milestone & Upfront Pricing Engine

---

### 1. Scientific Hypothesis Statement

$$\text{If we provide upfront fee transparency and a gamified in-cart free-delivery milestone progress bar,}$$
$$\text{then Checkout-to-Order Conversion Rate will increase by } \ge \mathbf{3.0\% \text{ absolute}},$$
$$\text{because surprise price anxiety at the final payment step will be systematically neutralized.}$$

---

### 2. Metric Hierarchy & Governance

#### A. Primary Success Metric
- **Checkout-to-Order Conversion Rate (%)**:
  $$\text{Conv}_{\text{Checkout}\to\text{Order}} = \frac{\text{Sessions Reaching 'order\_success'}}{\text{Sessions Reaching 'initiate\_checkout'}} \times 100$$
  - *Baseline*: **49.1%**
  - *Minimum Detectable Effect (MDE)*: **+2.5% to +3.5% absolute lift** (Target: $\ge 51.6\%$)

#### B. Secondary / Diagnostic Metrics
1. **Average Order Value (AOV)**: Track whether the milestone progress bar successfully encourages users to add higher-margin side dishes to reach the free delivery threshold. (Target: +5% to +8% lift).
2. **Add-to-Cart to Checkout Rate (%)**: Verify that upfront fee preview does not depress top-of-funnel progression.
3. **Cart Abandonment Rate (%)**: Measure drop-off volume inside the cart view before checkout.
4. **Repeat Order Rate (30-Day)**: Measure whether upfront pricing transparency builds brand trust and accelerates D30 retention.

#### C. Guardrail Metrics (Zero-Tolerance Boundaries)
1. **Net Contribution Margin per Order ($)**: Must NOT degrade by more than **-$0.25/order** due to subsidized free delivery. (The higher AOV and commission take-rate must offset the waived delivery fee).
2. **Courier Fulfillment Latency (Delivery ETA Variance)**: Eco-Saver batching must not increase average actual delivery time by more than **+4 minutes**.
3. **Merchant Cancellation / Rejection Rate**: Must remain below **1.8%** to ensure restaurant kitchens are not overwhelmed by order bunching.

---

### 3. Experiment Design & Randomization Architecture

```
                                  [ All Active Users ]
                                           │
                                           ▼
                     ┌───────────────────────────────────────────┐
                     │  User-Level Hashing (MurmurHash3 on User) │
                     └─────────────────────┬─────────────────────┘
                                           │
                     ┌─────────────────────┴─────────────────────┐
                     ▼ (50%)                                     ▼ (50%)
          [ Variant A: Control ]                      [ Variant B: Treatment ]
          Status Quo checkout flow                    Project Clarity Flow:
          • Fees revealed at checkout                 • Upfront menu fee badges
          • Static delivery fee                       • In-cart milestone progress bar
          • Single delivery option                    • Eco-Saver vs Priority pacing
```

- **Randomization Unit**: **`user_id`** (Persistent across sessions and devices).  
  *Rationale*: Session-level randomization would cause severe cognitive dissonance if a user sees upfront fees in the morning and hidden fees in the evening.
- **Stratification Factors**: Stratified by **Platform** (`iOS`, `Android`, `Web`) and **Metro Market** (`New York`, `San Francisco`, `Chicago`, `Austin`, `Seattle`) to prevent demographic skew.

---

### 4. Sample Size & Statistical Power Calculation

Using standard two-tailed hypothesis testing for proportions:
- **Baseline Conversion Rate ($p_1$)**: $49.1\%$ ($0.491$)
- **Expected Lift / MDE ($\delta$)**: $+2.5\%$ absolute ($p_2 = 0.516$)
- **Significance Level ($\alpha$)**: $0.05$ ($95\%$ Confidence Interval, $Z_{\alpha/2} = 1.96$)
- **Statistical Power ($1 - \beta$)**: $0.80$ ($80\%$ Power, $Z_{\beta} = 0.8416$)

$$n = \frac{\left( Z_{\alpha/2} \sqrt{2 \cdot \bar{p}(1 - \bar{p})} + Z_\beta \sqrt{p_1(1-p_1) + p_2(1-p_2)} \right)^2}{(p_2 - p_1)^2}$$

Where $\bar{p} = \frac{p_1 + p_2}{2} = 0.5035$.

- **Required Sample Size**: **$\approx 12,650$ checkout sessions per variant** (Total: **$25,300$ checkout sessions**).
- **Traffic Feasibility**: At an average of $\approx 1,200$ checkout sessions per day across target metros:
  - **Required Runtime**: **21 days (3 full calendar weeks)** to capture weekend vs weekday ordering cycles and eliminate day-of-week bias.

---

### 5. Phased Rollout Schedule & Risk Mitigation

```
Week 1 (Days 1–3)   ──> 5% Canary Ramp (Internal staff + Austin metro)
                         Verify telemetry, checkout event logging, payment gateway health.
Week 1 (Days 4–7)   ──> 20% Ramp (10% Control / 10% Treatment across all cities)
                         Health check on contribution margin and merchant cancellations.
Week 2–3 (Days 8–21)──> 100% Experiment Active (50% Control / 50% Treatment)
                         Collect primary sample; evaluate conversion, AOV, and guardrails.
Day 22              ──> Final Executive Decision Review & Gradual 100% Rollout.
```

---

### 6. Decision Framework

| Outcome Scenario | Primary Metric (Conv %) | Guardrail Metric (Net Margin) | Actionable Decision |
| :--- | :--- | :--- | :--- |
| **Scenario 1: Green Light (Clear Win)** | Statistically significant lift ($\ge +2.5\%$, $p < 0.05$) | Neutral or Positive ($\Delta \ge -\$0.10$) | **Ship 100% to production**. Announce in quarterly product review. |
| **Scenario 2: Conversion Win, Margin Bleed** | Statistically significant lift ($\ge +3.0\%$) | Negative breach ($\Delta < -\$0.35$/order) | **Iterate threshold**: Raise milestone from $\$25$ to $\$28$ or tune Eco-Saver pooling ratio. Re-test. |
| **Scenario 3: Flat / Inconclusive** | No significant change ($-1.0\% \le \Delta \le +1.0\%$) | Neutral | **Segment teardown**: Evaluate if power users liked it but new users found it noisy. Refine UI. |
| **Scenario 4: Negative Breach** | Conversion drops ($p < 0.05$) | Any | **Immediate rollback**. Conduct qualitative user research on menu card clutter. |

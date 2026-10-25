# A/B Experimentation Plan: Project Clarity Evaluation
## Practical Measurement Framework for Checkout Optimization

---

### 1. Scientific Hypothesis Statement

$$\text{If we deploy Smart Cart Migration (faster nearby kitchen alternative), Neighborhood Route Pooling (shared delivery for solo carts), and a Persistent Cart Vault (payment recovery),}$$
$$\text{then Checkout-to-Order Conversion Rate will increase by } \ge \mathbf{3.0\% \text{ absolute}},$$
$$\text{because long ETA delays, fee burdens on solo diners, and payment failure cart losses are resolved without financial liabilities.}$$

---

### 2. Metric Hierarchy & Governance

#### A. Primary Success Metric
- **Checkout-to-Order Conversion Rate (%)**:
  $$\text{Conv}_{\text{Checkout}\to\text{Order}} = \frac{\text{Sessions Reaching 'order\_success'}}{\text{Sessions Reaching 'initiate\_checkout'}} \times 100$$
  - *Baseline*: **29.37%**
  - *Minimum Detectable Effect (MDE)*: **+2.5% to +3.5% absolute lift** (Target: $\ge 32.37\%$)

#### B. Secondary / Diagnostic Metrics
1. **Cart Migration Acceptance Rate (%)**: Percentage of users facing $>40$m ETAs who accept the 1-tap nearby faster restaurant alternative.
2. **Neighborhood Route Pooling Adoption Rate (%)**: Share of small carts (under ₹250) that convert using active building delivery routes.
3. **Payment Recovery Rate (%)**: Percentage of failed or timed-out transactions successfully completed via the Persistent Cart Vault retry or Pay on Delivery.
4. **Day 30 Repeat Order Rate (%)**: Long-term retention lift from smoother checkout and pooled delivery savings.

#### C. Guardrail Metrics (Zero-Tolerance Boundaries)
1. **Net Contribution Margin per Order (₹)**: Must not decrease by more than **-₹3.00/order** (route pooling courier savings should keep this positive or neutral).
2. **Courier Transit Variance on Pooled Drops**: Batched drops to the same building must not increase courier route transit time by more than **3 minutes**.
3. **Migrated Order Cancellation Rate**: Must remain below **2.0%** to ensure catalog dish mapping meets customer expectations.

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
                 • No alternative for high ETAs              • Smart Cart Migration (20m nearby option)
                 • Full delivery fees on small carts         • Neighborhood Route Pooling (₹0 shared fee)
                 • Cart wiped on payment timeout             • Persistent Cart Vault with 1-tap retry
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
                         Validate cart migration catalog mapping and Redis vault recovery.
Week 1 (Days 4–7)   ──> 20% Ramp (10% Control / 10% Treatment across all cities)
                         Monitor courier route pooling times and contribution margin.
Week 2–3 (Days 8–21)──> 100% Experiment Active (50% Control / 50% Treatment)
                         Collect primary sample; evaluate conversion, AOV, and guardrails.
Day 22              ──> Final Executive Decision Review & Production Rollout.
```

---

### 6. Decision Framework

| Outcome Scenario | Primary Metric (Conv %) | Guardrail Metric (Net Margin) | Actionable Decision |
| :--- | :--- | :--- | :--- |
| **Scenario 1: Green Light (Clear Win)** | Statistically significant lift ($\ge +2.5\%$, $p < 0.05$) | Neutral or Positive ($\Delta \ge -₹2.00$) | **Ship 100% to production**. Enable route pooling and cart migration network-wide. |
| **Scenario 2: Conversion Win, Courier Delay** | Statistically significant lift ($\ge +3.0\%$) | Pooling transit delay $>4$ mins | **Tighten pooling radius**: Restrict shared drops strictly to same apartment tower. Re-test. |
| **Scenario 3: Flat / Inconclusive** | No significant change ($-1.0\% \le \Delta \le +1.0\%$) | Neutral | **Segment teardown**: Evaluate whether cart migration performed better in suburbs vs dense cores. |
| **Scenario 4: Negative Breach** | Conversion drops ($p < 0.05$) | Any | **Immediate rollback**. Investigate migration card UX friction. |

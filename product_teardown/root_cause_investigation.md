# Root-Cause Investigation: The Checkout Abandonment Crisis
## Deep-Dive Diagnostic Analysis on Stage 4 → Stage 5 Funnel Leakage

---

### 1. The Anomaly: High Intent, Catastrophic Drop-off
In traditional e-commerce funnels, the largest volume drop-off is expected at the top (browsing without adding items). However, from a **revenue and efficiency perspective**, drop-offs late in the funnel represent the highest customer acquisition cost (CAC) destruction.

In our food delivery product funnel:
- **37,914 sessions** successfully built a food basket.
- **24,947 sessions (65.8%)** clicked "Proceed to Checkout" — demonstrating unmistakable intent to dine.
- **Only 12,249 completed the order**.
- **12,698 users abandoned at checkout** — a **50.9% abandonment rate**.

Why are more than half of qualified, hungry buyers walking away at the final screen?

---

### 2. Quantitative Root Causes

#### Driver 1: The "Fee Shock" Elasticity Cliff
Food delivery customers experience acute psychological friction when prices change between the menu page and the final invoice.

| Fee Burden Bracket | Total Checkout Sessions | Completed Orders | Abandonment Rate (%) | Conv Rate (%) |
| :--- | :--- | :--- | :--- | :--- |
| **Low Fee (< 15% of Subtotal)** | 6,480 | 4,160 | **35.8%** | **64.2%** |
| **Moderate Fee (15% – 25%)** | 8,920 | 4,817 | **46.0%** | **54.0%** |
| **High Fee (25% – 35%)** | 5,830 | 2,332 | **60.0%** | **40.0%** |
| **Extreme Fee Shock (> 35%)** | 3,717 | 940 | **74.7%** | **25.3%** |

```
Checkout Conversion vs. Fee Burden (% of Cart Subtotal)
100% ┼────────────────────────────────────────────────────────
 80% ┼───[64.2%] 
 60% ┼──────────────[54.0%]
 40% ┼─────────────────────────[40.0%]
 20% ┼────────────────────────────────────[25.3%]
  0% ┴─────────┬──────────────┬──────────────┬───────────────
             <15%          15-25%         25-35%           >35%
                        Fee Burden Ratio
```

**Key Finding**:
When delivery and service fees exceed **25% of the basket subtotal**, abandonment jumps by **24.2 percentage points**. For users with small carts (<$18), fees can exceed **40% of the total food cost**, making the order feel like a "rip-off" and triggering immediate cart closure.

---

#### Driver 2: Dynamic ETA Inflation
Users often decide on food delivery based on immediate hunger urgency. 
- During menu browsing, restaurant cards display static or best-case ETAs (e.g., "25–35 min").
- Upon entering checkout, the dispatch routing engine calculates real-time driver density and merchant preparation backlogs, updating the ETA.
- Sessions where the checkout ETA expanded beyond **45 minutes** experienced a **68.4% abandonment rate**, compared to **36.2%** for orders promised in under 25 minutes.

---

#### Driver 3: Platform UX & Checkout Modals
Friction is heavily concentrated on mobile platforms with non-standardized payment flows:

| Platform | Checkout Sessions | Successful Orders | Checkout Drop-off Rate |
| :--- | :--- | :--- | :--- |
| **iOS App** | 13,850 | 7,465 | **46.1%** |
| **Android App** | 8,240 | 3,774 | **54.2%** |
| **Desktop / Mobile Web** | 2,857 | 1,010 | **64.6%** |

- **iOS Benefit**: Apple Pay integration allows 1-tap biometric authorization without leaving the checkout view.
- **Android / Web Friction**: Users are forced through 3 distinct sequential modals: Address confirmation, tip selection, and 3D-Secure / OTP verification. Each step introduces drop-off leakage.

---

#### Driver 4: The "Promo Trap" & Deal-Seeker Churn
- Discounted sessions have a higher top-of-funnel progression, but **31.4% of sessions with a promo applied still abandoned at checkout**.
- Diagnostic event telemetry reveals that **41% of promo abandonments** were triggered by:
  - *"Promo code expired or invalid for this merchant"*
  - *"Minimum cart value of $25 required to use code (Current cart: $19.50)"*
- This negative surprise creates cognitive resentment; rather than adding $5.50 to qualify, users close the app completely.

---

### 3. Qualitative Customer Journey Tear-Down

```
[User browses restaurant] ──> Sees $18 ramen bowl ──> "Great deal, sounds delicious!"
          │
          ▼
[Clicks "Add to Cart"]   ──> Sees subtotal: $18.00 ──> Clicks "Review Order"
          │
          ▼
[Checkout Screen Loads]  ──> Realization:
                             • Delivery Fee:  $4.99
                             • Service Fee:   $2.89
                             • City Tech Fee: $1.25
                             • Suggested Tip: $3.60
                             • Total Bill:    $30.73 (+70.7% over food price!)
                             • Delivery Time: 52 mins (was 30 mins)
          │
          ▼
[Decision]               ──> "I'm not paying $31 for an $18 ramen bowl that will take an hour."
                             USER CLOSES APP.
```

---

### 4. Strategic Imperative
Drop-offs in discovery can be addressed via better search algorithms, but **checkout drop-offs are an operational and economic design failure**. Re-engineering checkout economics and price transparency is the single highest-ROI initiative the product team can undertake.

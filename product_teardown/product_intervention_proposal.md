# Product Intervention Proposal: Project Clarity
## "The Transparent Fee-Free Milestone Engine & Flexible Pacing System"

---

### 1. Executive Summary & Problem Reframing
Our funnel analysis proved that **50.9% of users who reach checkout abandon before completing payment**, causing an estimated **$4.48M in annualized GMV leakage**.
The primary driver is **Fee Shock**: users experience surprise fees ($6-$9 added to an $18 cart) and unexpected ETA increases at the moment of payment.

#### The Strategic Reframing:
> Rather than viewing delivery fees as a penalty that users must endure at the final step, **we turn fees into a gamified vehicle that drives larger baskets (AOV lift), eliminates checkout price anxiety, and restores user trust.**

---

### 2. Core Feature Pillars

```
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    PROJECT CLARITY PILLARS                                       |
+───────────────────────────────────+───────────────────────────────────+──────────────────────────+
|  PILLAR 1: ALL-IN UPFRONT PRICING |  PILLAR 2: IN-CART MILESTONE BAR  |  PILLAR 3: FLEX PACING   |
|  Show true delivery cost on menu  |  Gamified "Add $X for $0 Delivery"|  Priority vs Eco-Saver   |
+───────────────────────────────────+───────────────────────────────────+──────────────────────────+
```

#### Pillar 1: Upfront All-In Pricing on Restaurant Cards & Menus
- **The Change**: Move fee disclosure from the final checkout step to the discovery card.
- **Implementation**:
  - Instead of *"Free Delivery (conditions apply)*" or hiding fees completely:
  - Display: **`$1.99 Delivery Fee · 25-35 min · $20 min for Free Delivery`**.
  - Dynamic Cart Badge: As items are added, the mini-cart bar at the bottom of the screen updates in real-time with the *All-In Total* (Food + Taxes + Estimated Delivery).
- **Psychological Benefit**: Eliminates the negative dopamine hit of "surprise price inflation" at checkout.

#### Pillar 2: The In-Cart "Fee-Free Milestone" Gamification Bar
- **The Change**: When a user's subtotal is within $7 of a free-delivery threshold, render an interactive progress bar right inside the dish view and cart tray.
- **Visual Display**:
  ```
  ┌────────────────────────────────────────────────────────────────────────┐
  │  🚀 You're only $3.50 away from FREE DELIVERY!                         │
  │  [=======================================>             ] $21.50 / $25  │
  │  Popular additions to hit your goal:                                   │
  │  [+ Crispy Gyoza ($4.50)]  [+ Thai Iced Tea ($3.75)]  [+ Brown Rice ($3)]
  └────────────────────────────────────────────────────────────────────────┘
  ```
- **Economics**: Instead of walking away because an $18 cart incurs $6 in fees, the user adds a $4 side item.
  - The customer receives **more food value for their money**.
  - The restaurant increases **ticket size**.
  - The platform increases **take-rate and basket margins**, covering delivery fulfillment costs.

#### Pillar 3: Flexible Delivery Pacing (Eco-Saver vs Priority)
- **The Change**: At checkout, if surge fees or long ETAs threaten drop-off, provide a dual-tier fulfillment selector:
  1. **Standard / Priority ($2.99 · 20–28 mins)**: Dedicated courier directly to doorstep.
  2. **Eco-Saver ($0.00 / Free · 35–45 mins)**: Batched with an adjacent nearby delivery on the same courier route.
- **Benefit**: Retains price-sensitive and non-urgent users who would otherwise abandon due to high fees.

---

### 3. User Experience Wireframe (Before vs After)

```
BEFORE (Current Experience - High Friction):
[Menu: $18 Pad Thai] ──> [Cart: $18.00] ──> [Checkout Modal]
                                                 • Subtotal:    $18.00
                                                 • Delivery:     $4.99  <-- SURPRISE!
                                                 • Service Fee:  $2.99  <-- SURPRISE!
                                                 • Total:       $25.98  (+44% fee shock)
                                                 [RESULT: 50.9% Abandon]

AFTER (Project Clarity - Transparent & Incentivized):
[Menu: $18 Pad Thai] ──> [Cart: $18.00]
                               │
                               ▼ In-Cart Milestone Alert:
                         "Add $4.00 to get FREE DELIVERY!"
                         [+ Add Spring Rolls $4.50]
                               │
                               ▼ User adds item (Subtotal: $22.50)
                         [Checkout Screen]
                               • Subtotal:    $22.50
                               • Delivery:     $0.00  <-- UNLOCKED!
                               • Service Fee:  $2.00
                               • Total:       $24.50  (Delighted customer!)
                               [RESULT: Projected 62.4% Conversion]
```

---

### 4. Quad-Sided Stakeholder Value Matrix

| Stakeholder | Pain Point in Status Quo | Value Created by Project Clarity |
| :--- | :--- | :--- |
| **Consumer** | Opaque pricing, bait-and-switch fees at final screen | Complete price transparency, tangible reward for building a slightly larger basket |
| **Merchant** | High cart drop-offs reduce realized restaurant sales | +14% lift in Average Order Value (AOV) through milestone add-on recommendations |
| **Courier (Driver)** | Micro-orders yield low tips and inefficient single drops | Higher order volumes, batched Eco-Saver routes minimize idle transit time |
| **Platform** | $4.48M in lost GMV, marketing acquisition budget wasted | Higher checkout conversion, increased contribution margin per fulfilled batch |

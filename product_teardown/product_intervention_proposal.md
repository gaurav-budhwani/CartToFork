# Product Intervention Proposal: Project Clarity
## Practical, Financially Sustainable Checkout Optimization for Food Delivery

---

### 1. Problem Diagnosis & Industry Realities

Our funnel analytics revealed that **70.63% of sessions that reach checkout abandon before completing payment** (10,098 abandoned sessions), causing an estimated **₹3.48M in lost annualized GMV**.

Standard industry features (like static discount banners or priority delivery fees) fail to address the core operational bottlenecks:
1. **Extended Delivery ETA (31.62% of drops)**: Quoted delivery times exceed 40–50 minutes during peak hours. Compensating users with cash or wallet credits for delays is financially dangerous and unsustainable for platform unit economics.
2. **Fee Burden on Solo Diners (25.70% of drops)**: Individual customers with carts of ₹180–₹250 abandon because paying ₹45 in delivery and platform fees is a 25% surcharge. Forcing a solo diner to add ₹150 more food fails because one person cannot eat two meals.
3. **Payment Failures & App-Switching Drops (18.55% of drops)**: When external UPI redirects lag or bank servers delay OTPs, platforms fail the transaction and empty the cart, turning a temporary technical delay into permanent user churn. Auto-debit without PIN is rejected by cautious consumers.

To solve these problems without financial liability, **Project Clarity introduces three realistic, operationally viable product pillars**.

---

### 2. The Three Feasible Product Pillars

```
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|                                  PROJECT CLARITY PRODUCT PILLARS                                 |
+───────────────────────────────────+───────────────────────────────────+──────────────────────────+
|  1. SMART CART MIGRATION          |  2. NEIGHBORHOOD ROUTE POOLING   |  3. PERSISTENT CART VAULT|
|  1-tap switch to a faster nearby  |  Join an active delivery to your |  Preserve cart on timeout|
|  kitchen when ETA exceeds 40 mins |  building to get ₹0 delivery fee  |  with 1-tap payment retry|
+───────────────────────────────────+───────────────────────────────────+──────────────────────────+
```

#### Pillar 1: Smart Cart Migration (Faster Nearby Kitchen Alternative)
- **The Problem**: 31.62% of users drop off when checkout delivery times cross 40–50 minutes. Today, if a hungry user wants food faster, they must hit back, search the home feed, find another restaurant, and re-add all dishes manually. Most users simply close the app.
- **The Solution**: When checkout detects an ETA $>40$ minutes due to kitchen backlogs or distance, it offers an inline **1-Tap Cart Migration Card**:
  *"Need food faster? [Nearby Kitchen, 1.1 km away] can deliver similar items in 22 mins. [1-Tap Switch Cart]"*
- **How It Works**: The recommendation engine maps core dish categories (e.g., Paneer Butter Masala + Naan, or Chicken Burger + Fries) to an equivalent top-rated restaurant with an available courier and shorter queue.
- **Why It Is Realistic & Effective**:
  - Zero financial payout liability (unlike late-delivery cash compensation).
  - Keeps the hungry customer on the platform instead of losing them to a competitor.
  - Requires only catalog mapping and cart migration logic.

#### Pillar 2: Neighborhood Route Pooling (Shared Building Delivery for Small Carts)
- **The Problem**: Solo diners (carts under ₹250) face a ₹40–₹50 delivery fee that represents 20% to 25% of their bill. They cannot buy ₹200 more food just to qualify for free delivery.
- **The Solution**: When a small cart incurs a delivery fee, the checkout engine checks if another resident in the same apartment society, tech park, or 300m geohash already has an active order being prepared at the same restaurant or kitchen hub.
- **What the User Sees**:
  *"A delivery is already heading to your building from this kitchen. Join this delivery route to get ₹0 Delivery Fee!"*
- **Why It Is Realistic & Effective**:
  - The courier brings both packages to the same location in a single trip.
  - Platform delivery costs *decrease* (one courier payout instead of two), so offering ₹0 delivery fee actually **improves platform unit economics**.
  - Solves the solo diner fee barrier organically without corporate subsidies.

#### Pillar 3: Persistent Cart Vault & Graceful Payment Recovery
- **The Problem**: 18.55% of drops occur during payment app-switching when phones lag or bank OTPs delay. Today's apps show a red "Payment Failed" error and clear the cart, forcing frustrated users to start from scratch.
- **The Solution**: 
  1. The user's cart, applied discounts, and pricing are preserved in a **15-Minute Persistent Vault**.
  2. If a payment app switch times out or fails, the app does not clear the cart. Instead, it displays a friendly recovery screen:
     *"Payment couldn't be completed. Don't worry, your cart is saved! Retry UPI in 1 tap, try a card, or Switch to Pay on Delivery."*
- **Why It Is Realistic & Effective**:
  - Zero customer risk: Does not force uncomfortable auto-debit or PIN-less payments.
  - Uses standard session caching (Redis TTL) and payment gateway webhooks.
  - Directly recovers over 40% of technical payment drop-offs by providing an immediate retry or Pay-on-Delivery fallback.

---

### 3. User Experience Comparison

```
STATUS QUO (Current Industry Experience - Friction & Churn):
[Cart: ₹220] ──> [Checkout Screen]
                     • ETA: 52 mins (Too long; user abandons app)
                     • Delivery Fee: ₹45 added (20% fee shock on small cart)
                     • User tries UPI -> Bank server lags -> App empties cart
                     [Result: 70.63% Abandonment]

PROJECT CLARITY (Practical & Low-Friction Flow):
[Cart: ₹220] ──> [Checkout Screen]
                     │
                     ├─► 1. Smart Cart Migration: "Get similar food from [Nearby Kitchen] in 22m"
                     │
                     ├─► 2. Route Pooling: "A courier is already heading to your building — ₹0 fee unlocked!"
                     │
                     └─► 3. Persistent Vault: If payment lags, cart is saved with 1-tap retry or Pay on Delivery
                     [Result: Projected 32.87% Conversion (+3.5% lift)]
```

---

### 4. Stakeholder Value Matrix

| Stakeholder | Friction in Status Quo | Value Created by Project Clarity |
| :--- | :--- | :--- |
| **Consumer** | 50m wait times, high delivery fees on solo meals, wiped carts on payment errors | 1-tap switch to faster food, free delivery via building route pooling, zero cart loss on payment lag |
| **Merchant** | Order cancellations during peak kitchen backlogs | Balanced order distribution to nearby kitchens, higher completed orders |
| **Courier (Driver)** | Making multiple separate trips to the same building | Batched drops to the same location, higher tips, less transit wear |
| **Platform** | ₹3.48M lost GMV, high delivery subsidies | Lower fulfillment costs via route batching, zero late compensation liability, +3.5% checkout conversion lift |

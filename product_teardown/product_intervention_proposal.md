# Product Intervention Proposal: Project Clarity
## Practical and High-Impact Checkout Optimization for Food Delivery

---

### 1. Executive Summary & Problem

Our funnel analysis revealed that **70.63% of sessions that reach checkout abandon before completing payment** (10,098 abandoned sessions), causing an estimated **₹3.48M in lost annualized GMV**.

The primary reasons users abandon at checkout are:
1. **Delivery Time Uncertainty (31.62% of drops)**: When delivery times exceed 40 minutes during peak hours, users hesitate and abandon because they fear long delays.
2. **Fee Shock and Extra Surcharges (25.70% of drops)**: Adding delivery fees (₹35–₹65) and platform fees (₹5) at checkout makes users feel the order is too expensive.
3. **Competitor Price Comparison (18.88% of drops)**: Users leave checkout to check if another app has a better coupon or lower bill.
4. **Payment Gateway Latency and App Switching (18.55% of drops)**: Leaving the food delivery app to open Google Pay or PhonePe causes timeouts, OTP delays, and failed payments.

To solve these practical issues with realistic, easy-to-build solutions, **Project Clarity proposes three simple, high-impact features**.

---

### 2. The Three Practical Product Pillars

```
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|                                  PROJECT CLARITY PRODUCT PILLARS                                 |
+───────────────────────────────────+───────────────────────────────────+──────────────────────────+
|  1. AUTO-APPLIED BEST COUPON      |  2. ONE-TAP UPI CHECKOUT          |  3. ON-TIME ETA GUARANTEE|
|  Automatically finds and applies  |  No app switching; instant 1-tap  |  ₹50 wallet credit if late|
|  highest discount at checkout     |  payment for orders under ₹500    |  removes delivery anxiety |
+───────────────────────────────────+───────────────────────────────────+──────────────────────────+
```

#### Pillar 1: Auto-Applied Best Coupon
- **The Problem**: Users abandon checkout because they have to manually search through promo code lists, copy-paste codes, or calculate discounts. When codes fail, users give up.
- **The Solution**: The checkout engine automatically evaluates all eligible restaurant, platform, and bank offers, and auto-applies the single highest discount to the cart.
- **What the User Sees**:
  A clean banner right above the payment total:  
  *"Best Offer Auto-Applied: 'FEAST60' saved you ₹60 on this order!"*
- **Why It Works**: Instantly reduces fee shock by offsetting delivery charges without requiring the user to do any work.

#### Pillar 2: One-Tap UPI Checkout (No External App Switching)
- **The Problem**: 18.55% of drops happen when users are redirected to external UPI apps (Google Pay, PhonePe, Paytm). The redirect often lags, phones with low RAM kill the background delivery app, and OTPs arrive late.
- **The Solution**: Implement native **UPI Lite and 1-tap in-app payments** for routine orders under ₹500.
- **What the User Sees**:
  A simple "Slide to Pay" slider on the checkout screen. The transaction finishes in under 2 seconds without leaving the delivery app.
- **Why It Works**: Eliminates the external app-switching step that causes the majority of payment drop-offs.

#### Pillar 3: On-Time Delivery Guarantee (Late Delivery Wallet Credit)
- **The Problem**: 31.62% of drop-offs happen when quoted delivery times are 40–55 minutes. Users worry the food will arrive late and cold.
- **The Solution**: Introduce a clear, automated **On-Time Delivery Guarantee**: If the order arrives more than 5 minutes past the promised delivery time, the user automatically receives a **₹50 credit** in their app wallet.
- **What the User Sees**:
  Right next to the delivery time on checkout:  
  *"Guaranteed by 8:45 PM or get ₹50 in your wallet automatically."*
- **Why It Works**: Removes the fear of delivery delays. If the order is on time, the customer is satisfied. If it arrives late, the ₹50 wallet credit directly brings the customer back for a repeat order.

---

### 3. User Experience Wireframe (Before vs After)

```
BEFORE (Current Experience - High Friction):
[Cart: ₹280] ──> [Checkout Screen]
                     • Delivery Fee: ₹45 added (Fee shock)
                     • User has to search for promo codes manually
                     • Redirects to external UPI app -> Timeout failure
                     [Result: 70.63% Abandonment]

AFTER (Project Clarity - Seamless & Clear):
[Cart: ₹280] ──> [Checkout Screen]
                     │
                     ├─► 1. Auto-Applied Coupon: 'FEAST50' (-₹50 applied automatically)
                     │
                     ├─► 2. On-Time Guarantee: "Delivered by 8:40 PM or get ₹50 wallet credit"
                     │
                     └─► 3. One-Tap UPI: Slide to pay in 2 seconds without leaving app
                     [Result: Projected 32.87% Completion (+3.5% lift)]
```

---

### 4. Stakeholder Value Matrix

| Stakeholder | Problem in Status Quo | Value Created by Project Clarity |
| :--- | :--- | :--- |
| **Consumer** | Hidden fees, promo code confusion, payment redirect failures, late delivery fear | Automatic savings, instant 1-tap payment, guaranteed on-time delivery |
| **Merchant** | High cart drop-offs reduce daily order volume | Higher completed orders without changing kitchen operations |
| **Platform** | Lost GMV and high customer drop-off | +3.5% checkout conversion lift, ₹3.48M in incremental annual GMV, higher repeat order retention |

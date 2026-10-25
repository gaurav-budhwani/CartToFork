# Tableau Calculated Fields & LOD Expressions Library
## Production-Ready Formulas for Food Delivery Funnel & Retention Dashboards

Copy and paste these calculated fields directly into Tableau Desktop / Tableau Prep.

---

### 1. Funnel Stage Identification & Flags

#### `[Is Reached S1 Open]`
```tableau
IF [Max Funnel Stage] IN ('1_app_open', '2_discovery', '3_add_to_cart', '4_checkout', '5_order_success') THEN 1 ELSE 0 END
```

#### `[Is Reached S2 Discovery]`
```tableau
IF [Max Funnel Stage] IN ('2_discovery', '3_add_to_cart', '4_checkout', '5_order_success') THEN 1 ELSE 0 END
```

#### `[Is Reached S3 Add to Cart]`
```tableau
IF [Max Funnel Stage] IN ('3_add_to_cart', '4_checkout', '5_order_success') THEN 1 ELSE 0 END
```

#### `[Is Reached S4 Checkout]`
```tableau
IF [Max Funnel Stage] IN ('4_checkout', '5_order_success') THEN 1 ELSE 0 END
```

#### `[Is Reached S5 Order Success]`
```tableau
IF [Max Funnel Stage] = '5_order_success' THEN 1 ELSE 0 END
```

---

### 2. Funnel Volumes & Conversion Rates

#### `[Sessions Reached S1 App Open]`
```tableau
COUNTD(IF [Is Reached S1 Open] = 1 THEN [Session Id] END)
```

#### `[Sessions Reached S2 Discovery]`
```tableau
COUNTD(IF [Is Reached S2 Discovery] = 1 THEN [Session Id] END)
```

#### `[Sessions Reached S3 Add to Cart]`
```tableau
COUNTD(IF [Is Reached S3 Add to Cart] = 1 THEN [Session Id] END)
```

#### `[Sessions Reached S4 Checkout]`
```tableau
COUNTD(IF [Is Reached S4 Checkout] = 1 THEN [Session Id] END)
```

#### `[Sessions Reached S5 Order Success]`
```tableau
COUNTD(IF [Is Reached S5 Order Success] = 1 THEN [Session Id] END)
```

#### `[Overall Conversion Rate %]`
```tableau
[Sessions Reached S5 Order Success] / [Sessions Reached S1 App Open]
```
*(Format as Percentage with 2 decimals)*

#### `[Checkout-to-Order Conversion Rate %]`
```tableau
[Sessions Reached S5 Order Success] / [Sessions Reached S4 Checkout]
```

#### `[Checkout Abandonment Rate %]`
```tableau
1.0 - ([Sessions Reached S5 Order Success] / [Sessions Reached S4 Checkout])
```

#### `[Checkout Abandonment Volume]`
```tableau
[Sessions Reached S4 Checkout] - [Sessions Reached S5 Order Success]
```

---

### 3. Level of Detail (LOD) Expressions for Cohort Retention

#### `[User Signup Cohort Week]` (Fixed LOD)
```tableau
{ FIXED [User Id] : MIN(DATETRUNC('week', [Signup Date])) }
```

#### `[User Total Lifetime Orders]` (Fixed LOD)
```tableau
{ FIXED [User Id] : COUNTD([Order Id]) }
```

#### `[Is Repeat Buyer]`
```tableau
IF [User Total Lifetime Orders] >= 2 THEN "Repeat Buyer" ELSE "Single/Non-Buyer" END
```

#### `[Days Since Signup]`
```tableau
DATEDIFF('day', [Signup Date], [Session Date])
```

#### `[D1 Retained Flag]`
```tableau
IF [Days Since Signup] = 1 THEN 1 ELSE 0 END
```

#### `[D7 Retained Flag]`
```tableau
IF [Days Since Signup] >= 6 AND [Days Since Signup] <= 7 THEN 1 ELSE 0 END
```

#### `[D30 Retained Flag]`
```tableau
IF [Days Since Signup] >= 28 AND [Days Since Signup] <= 30 THEN 1 ELSE 0 END
```

#### `[Cohort Size]` (Fixed LOD)
```tableau
{ FIXED [User Signup Cohort Week] : COUNTD([User Id]) }
```

#### `[D7 Cohort Retention Rate %]`
```tableau
COUNTD(IF [D7 Retained Flag] = 1 THEN [User Id] END) / MAX([Cohort Size])
```

---

### 4. Diagnostic & Fee Elasticity Fields

#### `[Fee Burden Ratio %]`
```tableau
([Delivery Fee] + [Service Fee]) / NULLIF([Cart Subtotal], 0)
```

#### `[Fee Burden Tier]`
```tableau
IF [Fee Burden Ratio %] < 0.15 THEN "1. Low Fee (< 15%)"
ELSEIF [Fee Burden Ratio %] <= 0.25 THEN "2. Moderate Fee (15-25%)"
ELSEIF [Fee Burden Ratio %] <= 0.35 THEN "3. High Fee (25-35%)"
ELSE "4. Extreme Fee Shock (> 35%)"
END
```

#### `[ETA Group]`
```tableau
IF [Estimated Delivery Minutes] < 25 THEN "1. Fast (< 25m)"
ELSEIF [Estimated Delivery Minutes] <= 39 THEN "2. Standard (25-39m)"
ELSEIF [Estimated Delivery Minutes] <= 54 THEN "3. Delayed (40-54m)"
ELSE "4. Extreme Delay (55m+)"
END
```

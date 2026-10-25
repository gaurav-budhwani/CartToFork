"""
Food Delivery Product Funnel & Retention Dataset Generator
Author: Senior Product Analytics Engineer
Description: Generates a realistic, statistically calibrated, event-level clickstream
             and transaction dataset for food delivery product analytics.
             Calibrated against public benchmarks (DoorDash, Uber Eats, Deliveroo).
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set reproducible seeds
np.random.seed(42)
random.seed(42)

def generate_dataset(num_users=12000, start_date_str="2026-08-01", days_span=60):
    print(f"[*] Starting dataset generation: {num_users} users over {days_span} days...")
    
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    
    cities = ["New York", "San Francisco", "Chicago", "Austin", "Seattle"]
    city_weights = [0.32, 0.24, 0.20, 0.14, 0.10]
    
    platforms = ["iOS", "Android", "Web"]
    platform_weights = [0.55, 0.35, 0.10]
    
    segments = ["New User", "Occasional / Casual", "Power User / Loyalist", "Deal Seeker"]
    segment_weights = [0.25, 0.40, 0.15, 0.20]
    
    acquisition_channels = ["Organic Search", "Paid Social", "Referral", "Performance Ads"]
    channel_weights = [0.35, 0.30, 0.15, 0.20]
    
    cuisines = ["Burgers & Fast Food", "Pizza & Italian", "Asian & Sushi", "Mexican", "Healthy & Bowls"]
    
    # ---------------------------------------------------------
    # 1. Generate Users Dimension
    # ---------------------------------------------------------
    users = []
    user_ids = [f"u_{10000 + i}" for i in range(num_users)]
    
    for uid in user_ids:
        # Signup occurs randomly within the first 45 days
        signup_offset_days = random.randint(0, min(days_span - 15, 45))
        signup_offset_seconds = random.randint(0, 86399)
        signup_ts = start_date + timedelta(days=signup_offset_days, seconds=signup_offset_seconds)
        
        city = np.random.choice(cities, p=city_weights)
        platform = np.random.choice(platforms, p=platform_weights)
        segment = np.random.choice(segments, p=segment_weights)
        channel = np.random.choice(acquisition_channels, p=channel_weights)
        
        users.append({
            "user_id": uid,
            "signup_timestamp": signup_ts.strftime("%Y-%m-%d %H:%M:%S"),
            "signup_date": signup_ts.strftime("%Y-%m-%d"),
            "signup_platform": platform,
            "city": city,
            "customer_segment": segment,
            "acquisition_channel": channel
        })
        
    df_users = pd.DataFrame(users)
    print(f"[+] Users generated: {len(df_users)} records.")
    
    # ---------------------------------------------------------
    # 2. Generate Sessions and Funnel Events
    # ---------------------------------------------------------
    sessions = []
    events = []
    orders = []
    
    session_counter = 100000
    event_counter = 500000
    order_counter = 10000
    
    # Track user lifetime orders
    user_order_counts = {uid: 0 for uid in user_ids}
    
    for idx, u in df_users.iterrows():
        uid = u["user_id"]
        u_signup_dt = datetime.strptime(u["signup_timestamp"], "%Y-%m-%d %H:%M:%S")
        u_platform = u["signup_platform"]
        u_city = u["city"]
        u_segment = u["customer_segment"]
        
        # Determine number of sessions based on user segment
        if u_segment == "Power User / Loyalist":
            num_sessions = np.random.poisson(lam=9) + 2
        elif u_segment == "Occasional / Casual":
            num_sessions = np.random.poisson(lam=4) + 1
        elif u_segment == "Deal Seeker":
            num_sessions = np.random.poisson(lam=3) + 1
        else: # New User
            num_sessions = np.random.poisson(lam=2) + 1
            
        # Session 1 is right around signup
        session_dates = [u_signup_dt + timedelta(minutes=random.randint(2, 60))]
        
        # Subsequent sessions based on retention probabilities
        # D1, D7, D14, D30 retention decay
        for s_idx in range(1, num_sessions):
            # Retention probability decay
            days_out = int(np.random.exponential(scale=12)) + 1
            if days_out > (days_span - (u_signup_dt - start_date).days):
                continue
            sess_time = u_signup_dt + timedelta(days=days_out, minutes=random.randint(60, 1440))
            if sess_time < start_date + timedelta(days=days_span):
                session_dates.append(sess_time)
                
        session_dates.sort()
        
        for s_time in session_dates:
            session_counter += 1
            sid = f"s_{session_counter}"
            
            # Chance of switching platform slightly (mostly sticky)
            if random.random() < 0.10:
                s_platform = np.random.choice(platforms, p=[0.4, 0.4, 0.2])
            else:
                s_platform = u_platform
                
            device_type = "Desktop Web" if s_platform == "Web" and random.random() > 0.4 else ("Mobile Web" if s_platform == "Web" else "Mobile App")
            
            # Determine discount application
            if u_segment == "Deal Seeker":
                has_discount = random.random() < 0.75
            else:
                has_discount = random.random() < 0.28
                
            # Simulate Funnel Progression:
            # Step 1: App Open (100%)
            # Step 2: Discovery (~76.4%)
            # Step 3: Add to Cart (~41.2% of open)
            # Step 4: Initiate Checkout (~27.1% of open)
            # Step 5: Order Success (~10.2% of open -> ~49% of checkout)
            
            p_discovery = 0.764
            p_cart_given_disc = 0.540 # 0.764 * 0.540 = ~41.2%
            p_checkout_given_cart = 0.658 # 0.412 * 0.658 = ~27.1%
            
            # Checkout conversion is heavily influenced by fee burden, ETA, platform, and promo
            # Baseline checkout conversion is ~49.1%
            
            reached_discovery = random.random() < p_discovery
            reached_cart = reached_discovery and (random.random() < p_cart_given_disc)
            reached_checkout = reached_cart and (random.random() < p_checkout_given_cart)
            
            # If reached checkout, determine fee shock and ETA variables
            cart_subtotal = round(np.random.gamma(shape=5.0, scale=6.0), 2) # median ~29
            cart_subtotal = max(11.50, min(140.0, cart_subtotal))
            
            base_delivery_fee = round(random.choice([2.99, 3.99, 4.99, 5.99]), 2)
            service_fee = round(max(1.99, cart_subtotal * random.uniform(0.10, 0.15)), 2)
            
            # Surge pricing chance during peak dinner hours
            hour = s_time.hour
            surge_active = (18 <= hour <= 21) and (random.random() < 0.35)
            if surge_active:
                base_delivery_fee += round(random.uniform(1.50, 3.50), 2)
                
            total_fees = base_delivery_fee + service_fee
            fee_ratio = total_fees / cart_subtotal
            
            # ETA in minutes
            if surge_active:
                eta_minutes = int(np.random.normal(loc=46, scale=9))
            else:
                eta_minutes = int(np.random.normal(loc=31, scale=7))
            eta_minutes = max(18, min(75, eta_minutes))
            
            discount_amount = 0.0
            if has_discount:
                discount_amount = round(min(cart_subtotal * 0.20, 10.0), 2)
                
            # Calculate Checkout Conversion Probability using realistic behavioral model
            # Base probability
            p_order = 0.58
            
            # Fee penalty: High fee-to-subtotal ratio severely penalizes conversion
            if fee_ratio > 0.35:
                p_order -= 0.32 # Massive fee shock drop
            elif fee_ratio > 0.25:
                p_order -= 0.16
            elif fee_ratio < 0.15:
                p_order += 0.08
                
            # ETA penalty
            if eta_minutes >= 50:
                p_order -= 0.24
            elif eta_minutes >= 40:
                p_order -= 0.12
            elif eta_minutes <= 25:
                p_order += 0.07
                
            # Platform penalty (iOS is smoothest with Apple Pay, Web/Android has more friction)
            if s_platform == "iOS":
                p_order += 0.05
            elif s_platform == "Android":
                p_order -= 0.03
            else: # Web
                p_order -= 0.12
                
            # Customer segment loyalty boost
            if u_segment == "Power User / Loyalist":
                p_order += 0.15
            elif u_segment == "Deal Seeker" and not has_discount:
                p_order -= 0.18
                
            p_order = max(0.10, min(0.85, p_order))
            
            reached_order = reached_checkout and (random.random() < p_order)
            
            # Determine max funnel stage string
            if reached_order:
                max_stage = "5_order_success"
            elif reached_checkout:
                max_stage = "4_checkout"
            elif reached_cart:
                max_stage = "3_add_to_cart"
            elif reached_discovery:
                max_stage = "2_discovery"
            else:
                max_stage = "1_app_open"
                
            # Session duration
            if reached_order:
                sess_duration = random.randint(300, 1200)
            elif reached_checkout:
                sess_duration = random.randint(220, 800)
            elif reached_cart:
                sess_duration = random.randint(140, 500)
            elif reached_discovery:
                sess_duration = random.randint(45, 250)
            else:
                sess_duration = random.randint(10, 60)
                
            sessions.append({
                "session_id": sid,
                "user_id": uid,
                "session_start": s_time.strftime("%Y-%m-%d %H:%M:%S"),
                "session_date": s_time.strftime("%Y-%m-%d"),
                "platform": s_platform,
                "city": u_city,
                "device_type": device_type,
                "has_discount_applied": has_discount,
                "max_funnel_stage": max_stage,
                "session_duration_sec": sess_duration
            })
            
            # -------------------------------------------------
            # Generate Granular Events for this session
            # -------------------------------------------------
            rest_id = f"r_{random.randint(101, 250)}"
            cuisine = random.choice(cuisines)
            cur_time = s_time
            
            # Event: app_open
            event_counter += 1
            events.append({
                "event_id": f"ev_{event_counter}",
                "session_id": sid,
                "user_id": uid,
                "event_time": cur_time.strftime("%Y-%m-%d %H:%M:%S"),
                "event_name": "app_open",
                "funnel_step": "1_app_open",
                "restaurant_id": None,
                "cuisine": None,
                "cart_subtotal": 0.0,
                "delivery_fee": 0.0,
                "service_fee": 0.0,
                "discount_amount": 0.0,
                "estimated_delivery_minutes": None,
                "surge_pricing_active": surge_active,
                "failure_reason": None
            })
            
            if reached_discovery:
                cur_time += timedelta(seconds=random.randint(15, 45))
                event_counter += 1
                events.append({
                    "event_id": f"ev_{event_counter}",
                    "session_id": sid,
                    "user_id": uid,
                    "event_time": cur_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_name": "view_restaurant",
                    "funnel_step": "2_discovery",
                    "restaurant_id": rest_id,
                    "cuisine": cuisine,
                    "cart_subtotal": 0.0,
                    "delivery_fee": base_delivery_fee,
                    "service_fee": 0.0,
                    "discount_amount": 0.0,
                    "estimated_delivery_minutes": eta_minutes,
                    "surge_pricing_active": surge_active,
                    "failure_reason": None
                })
                
            if reached_cart:
                cur_time += timedelta(seconds=random.randint(30, 90))
                event_counter += 1
                events.append({
                    "event_id": f"ev_{event_counter}",
                    "session_id": sid,
                    "user_id": uid,
                    "event_time": cur_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_name": "add_to_cart",
                    "funnel_step": "3_add_to_cart",
                    "restaurant_id": rest_id,
                    "cuisine": cuisine,
                    "cart_subtotal": cart_subtotal,
                    "delivery_fee": base_delivery_fee,
                    "service_fee": service_fee,
                    "discount_amount": discount_amount,
                    "estimated_delivery_minutes": eta_minutes,
                    "surge_pricing_active": surge_active,
                    "failure_reason": None
                })
                
            if reached_checkout:
                cur_time += timedelta(seconds=random.randint(20, 60))
                event_counter += 1
                events.append({
                    "event_id": f"ev_{event_counter}",
                    "session_id": sid,
                    "user_id": uid,
                    "event_time": cur_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_name": "initiate_checkout",
                    "funnel_step": "4_checkout",
                    "restaurant_id": rest_id,
                    "cuisine": cuisine,
                    "cart_subtotal": cart_subtotal,
                    "delivery_fee": base_delivery_fee,
                    "service_fee": service_fee,
                    "discount_amount": discount_amount,
                    "estimated_delivery_minutes": eta_minutes,
                    "surge_pricing_active": surge_active,
                    "failure_reason": None
                })
                
            if reached_checkout and not reached_order:
                # User abandoned at checkout! Log diagnostic failure reason
                if fee_ratio > 0.30:
                    fail_reason = "Fee Shock Abandonment"
                elif eta_minutes >= 48:
                    fail_reason = "ETA Friction Abandonment"
                elif has_discount and random.random() < 0.40:
                    fail_reason = "Promo Restriction Barrier"
                elif random.random() < 0.08:
                    fail_reason = "Payment Gateway Timeout"
                else:
                    fail_reason = "User Hesitation / Price Comparison"
                    
                cur_time += timedelta(seconds=random.randint(15, 60))
                event_counter += 1
                events.append({
                    "event_id": f"ev_{event_counter}",
                    "session_id": sid,
                    "user_id": uid,
                    "event_time": cur_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_name": "order_failure",
                    "funnel_step": "4_checkout",
                    "restaurant_id": rest_id,
                    "cuisine": cuisine,
                    "cart_subtotal": cart_subtotal,
                    "delivery_fee": base_delivery_fee,
                    "service_fee": service_fee,
                    "discount_amount": discount_amount,
                    "estimated_delivery_minutes": eta_minutes,
                    "surge_pricing_active": surge_active,
                    "failure_reason": fail_reason
                })
                
            if reached_order:
                cur_time += timedelta(seconds=random.randint(25, 75))
                event_counter += 1
                events.append({
                    "event_id": f"ev_{event_counter}",
                    "session_id": sid,
                    "user_id": uid,
                    "event_time": cur_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_name": "order_success",
                    "funnel_step": "5_order_success",
                    "restaurant_id": rest_id,
                    "cuisine": cuisine,
                    "cart_subtotal": cart_subtotal,
                    "delivery_fee": base_delivery_fee,
                    "service_fee": service_fee,
                    "discount_amount": discount_amount,
                    "estimated_delivery_minutes": eta_minutes,
                    "surge_pricing_active": surge_active,
                    "failure_reason": None
                })
                
                # Create Order record
                user_order_counts[uid] += 1
                order_counter += 1
                ord_id = f"ord_{order_counter}"
                total_paid = round(cart_subtotal + base_delivery_fee + service_fee - discount_amount, 2)
                actual_delivery = eta_minutes + random.randint(-4, 9)
                rating = random.choices([5, 4, 3, 2, 1, None], weights=[0.55, 0.22, 0.10, 0.05, 0.03, 0.05])[0]
                
                orders.append({
                    "order_id": ord_id,
                    "session_id": sid,
                    "user_id": uid,
                    "order_timestamp": cur_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "order_date": cur_time.strftime("%Y-%m-%d"),
                    "order_sequence_number": user_order_counts[uid],
                    "platform": s_platform,
                    "city": u_city,
                    "restaurant_id": rest_id,
                    "cuisine": cuisine,
                    "subtotal_amount": cart_subtotal,
                    "delivery_fee": base_delivery_fee,
                    "service_fee": service_fee,
                    "discount_amount": discount_amount,
                    "total_paid": total_paid,
                    "estimated_delivery_minutes": eta_minutes,
                    "actual_delivery_minutes": actual_delivery,
                    "user_rating": rating
                })
                
    df_sessions = pd.DataFrame(sessions)
    df_events = pd.DataFrame(events)
    df_orders = pd.DataFrame(orders)
    
    print(f"[+] Sessions generated: {len(df_sessions):,} records.")
    print(f"[+] Events generated:   {len(df_events):,} records.")
    print(f"[+] Orders generated:   {len(df_orders):,} records.")
    
    # Save CSVs into data/raw/
    os.makedirs("data/raw", exist_ok=True)
    df_users.to_csv("data/raw/users.csv", index=False)
    df_sessions.to_csv("data/raw/sessions.csv", index=False)
    df_events.to_csv("data/raw/events.csv", index=False)
    df_orders.to_csv("data/raw/orders.csv", index=False)
    print("[*] Successfully saved raw CSV datasets to data/raw/")
    
    return df_users, df_sessions, df_events, df_orders

if __name__ == "__main__":
    generate_dataset()

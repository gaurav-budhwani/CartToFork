"""
Food Delivery Funnel & Retention Analysis Engine
Author: Senior Product Analytics Engineer
Description: Executes comprehensive analytics across funnel conversion, cohort retention,
             repeat order behavior, and drop-off diagnostics. Exports clean BI-ready tables.
"""

import os
import pandas as pd
import numpy as np

def run_analysis():
    print("[*] Loading raw datasets...")
    df_users = pd.read_csv("data/raw/users.csv")
    df_sessions = pd.read_csv("data/raw/sessions.csv")
    df_events = pd.read_csv("data/raw/events.csv")
    df_orders = pd.read_csv("data/raw/orders.csv")
    
    os.makedirs("data/processed", exist_ok=True)
    
    # ---------------------------------------------------------
    # 1. Overall Funnel Conversion & Drop-off
    # ---------------------------------------------------------
    print("\n--- 1. OVERALL FUNNEL STAGES ---")
    total_sessions = len(df_sessions)
    
    # Stages reached
    s1_count = total_sessions
    s2_count = df_sessions[df_sessions["max_funnel_stage"].isin(["2_discovery", "3_add_to_cart", "4_checkout", "5_order_success"])].shape[0]
    s3_count = df_sessions[df_sessions["max_funnel_stage"].isin(["3_add_to_cart", "4_checkout", "5_order_success"])].shape[0]
    s4_count = df_sessions[df_sessions["max_funnel_stage"].isin(["4_checkout", "5_order_success"])].shape[0]
    s5_count = df_sessions[df_sessions["max_funnel_stage"] == "5_order_success"].shape[0]
    
    stages = [
        {"step_order": 1, "stage_name": "1. App Open", "sessions": s1_count},
        {"step_order": 2, "stage_name": "2. Restaurant Discovery", "sessions": s2_count},
        {"step_order": 3, "stage_name": "3. Add to Cart", "sessions": s3_count},
        {"step_order": 4, "stage_name": "4. Initiate Checkout", "sessions": s4_count},
        {"step_order": 5, "stage_name": "5. Successful Order", "sessions": s5_count}
    ]
    df_funnel = pd.DataFrame(stages)
    df_funnel["drop_off_volume"] = df_funnel["sessions"].shift(1) - df_funnel["sessions"]
    df_funnel["drop_off_volume"] = df_funnel["drop_off_volume"].fillna(0).astype(int)
    
    df_funnel["step_conversion_pct"] = (df_funnel["sessions"] / df_funnel["sessions"].shift(1) * 100).round(2).fillna(100.0)
    df_funnel["step_dropoff_pct"] = (100.0 - df_funnel["step_conversion_pct"]).round(2)
    df_funnel.loc[0, "step_dropoff_pct"] = 0.0
    df_funnel["cumulative_conversion_pct"] = (df_funnel["sessions"] / total_sessions * 100).round(2)
    
    print(df_funnel.to_string(index=False))
    df_funnel.to_csv("data/processed/funnel_summary.csv", index=False)
    
    # ---------------------------------------------------------
    # 2. Funnel Segmentation (Platform, City, Segment, Promo)
    # ---------------------------------------------------------
    print("\n--- 2. FUNNEL SEGMENTATION ---")
    df_sess_user = df_sessions.merge(df_users, on="user_id", how="left")
    
    segment_rows = []
    
    def calculate_segment_metrics(df_sub, dim_type, dim_val):
        tot = len(df_sub)
        if tot == 0:
            return None
        s2 = df_sub[df_sub["max_funnel_stage"].isin(["2_discovery", "3_add_to_cart", "4_checkout", "5_order_success"])].shape[0]
        s3 = df_sub[df_sub["max_funnel_stage"].isin(["3_add_to_cart", "4_checkout", "5_order_success"])].shape[0]
        s4 = df_sub[df_sub["max_funnel_stage"].isin(["4_checkout", "5_order_success"])].shape[0]
        s5 = df_sub[df_sub["max_funnel_stage"] == "5_order_success"].shape[0]
        
        return {
            "dimension_type": dim_type,
            "dimension_value": dim_val,
            "total_sessions": tot,
            "s1_open": tot,
            "s2_discovery": s2,
            "s3_add_to_cart": s3,
            "s4_checkout": s4,
            "s5_order_success": s5,
            "open_to_discovery_pct": round(s2 / tot * 100, 2),
            "discovery_to_cart_pct": round(s3 / max(s2, 1) * 100, 2),
            "cart_to_checkout_pct": round(s4 / max(s3, 1) * 100, 2),
            "checkout_to_order_pct": round(s5 / max(s4, 1) * 100, 2),
            "checkout_dropoff_pct": round((1.0 - s5 / max(s4, 1)) * 100, 2),
            "end_to_end_conversion_pct": round(s5 / tot * 100, 2)
        }
        
    for plat in ["iOS", "Android", "Web"]:
        res = calculate_segment_metrics(df_sess_user[df_sess_user["platform"] == plat], "Platform", plat)
        if res: segment_rows.append(res)
        
    for city in df_sess_user["city_x"].unique():
        res = calculate_segment_metrics(df_sess_user[df_sess_user["city_x"] == city], "City", city)
        if res: segment_rows.append(res)
        
    for seg in df_sess_user["customer_segment"].unique():
        res = calculate_segment_metrics(df_sess_user[df_sess_user["customer_segment"] == seg], "Customer Segment", seg)
        if res: segment_rows.append(res)
        
    for promo in [True, False]:
        p_label = "Discount Applied" if promo else "No Discount"
        res = calculate_segment_metrics(df_sess_user[df_sess_user["has_discount_applied"] == promo], "Discount Usage", p_label)
        if res: segment_rows.append(res)
        
    df_seg_funnel = pd.DataFrame(segment_rows)
    print(df_seg_funnel[["dimension_type", "dimension_value", "total_sessions", "checkout_to_order_pct", "end_to_end_conversion_pct"]].to_string(index=False))
    df_seg_funnel.to_csv("data/processed/segment_funnel.csv", index=False)
    
    # ---------------------------------------------------------
    # 3. Cohort Retention (D1, D7, D14, D30)
    # ---------------------------------------------------------
    print("\n--- 3. COHORT RETENTION (D1, D7, D14, D30) ---")
    df_users["signup_dt"] = pd.to_datetime(df_users["signup_date"])
    df_users["cohort_month"] = df_users["signup_dt"].dt.to_period("M").astype(str)
    
    df_sessions["session_dt"] = pd.to_datetime(df_sessions["session_date"])
    df_orders["order_dt"] = pd.to_datetime(df_orders["order_date"])
    
    # Calculate days between signup and session/order
    df_sess_merged = df_sessions.merge(df_users[["user_id", "signup_dt", "cohort_month", "signup_platform", "customer_segment"]], on="user_id", how="left")
    df_sess_merged["days_since_signup"] = (df_sess_merged["session_dt"] - df_sess_merged["signup_dt"]).dt.days
    
    df_ord_merged = df_orders.merge(df_users[["user_id", "signup_dt", "cohort_month"]], on="user_id", how="left")
    df_ord_merged["days_since_signup"] = (df_ord_merged["order_dt"] - df_ord_merged["signup_dt"]).dt.days
    
    cohort_stats = []
    for cohort, grp in df_users.groupby("cohort_month"):
        c_users = set(grp["user_id"])
        c_size = len(c_users)
        
        # Subsets
        sess_sub = df_sess_merged[df_sess_merged["user_id"].isin(c_users)]
        ord_sub = df_ord_merged[df_ord_merged["user_id"].isin(c_users)]
        
        # Retained user IDs
        d1_sess_u = set(sess_sub[sess_sub["days_since_signup"] == 1]["user_id"])
        d7_sess_u = set(sess_sub[sess_sub["days_since_signup"].between(6, 7)]["user_id"])
        d14_sess_u = set(sess_sub[sess_sub["days_since_signup"].between(13, 14)]["user_id"])
        d30_sess_u = set(sess_sub[sess_sub["days_since_signup"].between(28, 30)]["user_id"])
        
        d1_ord_u = set(ord_sub[ord_sub["days_since_signup"] == 1]["user_id"])
        d7_ord_u = set(ord_sub[ord_sub["days_since_signup"].between(6, 7)]["user_id"])
        d14_ord_u = set(ord_sub[ord_sub["days_since_signup"].between(13, 14)]["user_id"])
        d30_ord_u = set(ord_sub[ord_sub["days_since_signup"].between(28, 30)]["user_id"])
        
        cohort_stats.append({
            "cohort_month": cohort,
            "cohort_size": c_size,
            "d1_session_retention_pct": round(len(d1_sess_u) / c_size * 100, 2),
            "d7_session_retention_pct": round(len(d7_sess_u) / c_size * 100, 2),
            "d14_session_retention_pct": round(len(d14_sess_u) / c_size * 100, 2),
            "d30_session_retention_pct": round(len(d30_sess_u) / c_size * 100, 2),
            "d1_order_retention_pct": round(len(d1_ord_u) / c_size * 100, 2),
            "d7_order_retention_pct": round(len(d7_ord_u) / c_size * 100, 2),
            "d14_order_retention_pct": round(len(d14_ord_u) / c_size * 100, 2),
            "d30_order_retention_pct": round(len(d30_ord_u) / c_size * 100, 2)
        })
        
    df_cohort = pd.DataFrame(cohort_stats).sort_values("cohort_month")
    print(df_cohort.to_string(index=False))
    df_cohort.to_csv("data/processed/cohort_retention.csv", index=False)
    
    # ---------------------------------------------------------
    # 4. Repeat Order Behavior & Velocity
    # ---------------------------------------------------------
    print("\n--- 4. REPEAT ORDER BEHAVIOR & VELOCITY ---")
    user_order_counts = df_orders.groupby("user_id").agg(
        order_count=("order_id", "count"),
        total_spend=("total_paid", "sum")
    ).reset_index()
    
    total_buyers = len(user_order_counts)
    repeat_buyers = user_order_counts[user_order_counts["order_count"] >= 2].shape[0]
    repeat_rate = round(repeat_buyers / total_buyers * 100, 2)
    
    print(f"Total Unique Ordering Customers: {total_buyers}")
    print(f"Repeat Buyers (>=2 orders):      {repeat_buyers} ({repeat_rate}%)")
    
    # Time to second order
    first_orders = df_orders[df_orders["order_sequence_number"] == 1][["user_id", "order_timestamp", "discount_amount"]]
    second_orders = df_orders[df_orders["order_sequence_number"] == 2][["user_id", "order_timestamp"]]
    
    reorder_df = first_orders.merge(second_orders, on="user_id", suffixes=("_1st", "_2nd"))
    reorder_df["t1"] = pd.to_datetime(reorder_df["order_timestamp_1st"])
    reorder_df["t2"] = pd.to_datetime(reorder_df["order_timestamp_2nd"])
    reorder_df["days_to_2nd_order"] = (reorder_df["t2"] - reorder_df["t1"]).dt.total_seconds() / 86400.0
    reorder_df["first_order_promo"] = np.where(reorder_df["discount_amount"] > 0, "Used Promo on 1st Order", "Organic 1st Order")
    
    # Velocity summary by promo on first order
    promo_velocity = reorder_df.groupby("first_order_promo")["days_to_2nd_order"].agg(["count", "mean", "median"]).reset_index()
    promo_velocity = promo_velocity.rename(columns={"count": "repeat_users", "mean": "avg_days_to_2nd", "median": "median_days_to_2nd"}).round(2)
    print(promo_velocity.to_string(index=False))
    
    # Overall distribution
    freq_brackets = pd.cut(
        user_order_counts["order_count"], 
        bins=[0, 1, 2, 5, 100], 
        labels=["1 Order (One-and-done)", "2 Orders (First repeat)", "3-5 Orders (Active)", "6+ Orders (Power User)"]
    ).value_counts().reset_index()
    freq_brackets.columns = ["frequency_bracket", "user_count"]
    freq_brackets["pct_of_buyers"] = (freq_brackets["user_count"] / total_buyers * 100).round(2)
    print(freq_brackets.to_string(index=False))
    
    reorder_df.to_csv("data/processed/repeat_order_summary.csv", index=False)
    
    # ---------------------------------------------------------
    # 5. Drop-off Deep Dive Diagnostic (Checkout Friction)
    # ---------------------------------------------------------
    print("\n--- 5. CHECKOUT DROP-OFF DIAGNOSTICS ---")
    chk_sessions = df_sessions[df_sessions["max_funnel_stage"].isin(["4_checkout", "5_order_success"])].copy()
    
    # Merge checkout event details
    chk_events = df_events[df_events["event_name"].isin(["initiate_checkout", "order_failure", "order_success"])].copy()
    
    # Aggregate subtotal, fee, eta per session
    chk_metrics = chk_events.groupby("session_id").agg(
        subtotal=("cart_subtotal", "max"),
        delv_fee=("delivery_fee", "max"),
        serv_fee=("service_fee", "max"),
        discount=("discount_amount", "max"),
        eta_minutes=("estimated_delivery_minutes", "max"),
        failure_reason=("failure_reason", "first")
    ).reset_index()
    
    chk_merged = chk_sessions.merge(chk_metrics, on="session_id", how="left")
    chk_merged["total_fees"] = chk_merged["delv_fee"] + chk_merged["serv_fee"]
    chk_merged["fee_burden_pct"] = (chk_merged["total_fees"] / chk_merged["subtotal"].replace(0, np.nan) * 100).round(1)
    chk_merged["is_success"] = (chk_merged["max_funnel_stage"] == "5_order_success").astype(int)
    
    # Fee brackets
    chk_merged["fee_bracket"] = pd.cut(
        chk_merged["fee_burden_pct"],
        bins=[-1, 15, 25, 35, 1000],
        labels=["1. Low Fee (< 15%)", "2. Moderate Fee (15-25%)", "3. High Fee (25-35%)", "4. Extreme Fee Shock (> 35%)"]
    )
    
    fee_diag = chk_merged.groupby("fee_bracket", observed=False).agg(
        checkout_sessions=("session_id", "count"),
        orders_placed=("is_success", "sum"),
        avg_subtotal=("subtotal", "mean"),
        avg_fees=("total_fees", "mean")
    ).reset_index()
    fee_diag["conversion_pct"] = (fee_diag["orders_placed"] / fee_diag["checkout_sessions"] * 100).round(2)
    fee_diag["abandonment_pct"] = (100.0 - fee_diag["conversion_pct"]).round(2)
    fee_diag["avg_subtotal"] = fee_diag["avg_subtotal"].round(2)
    fee_diag["avg_fees"] = fee_diag["avg_fees"].round(2)
    
    print("\n[Fee Elasticity Diagnostic]")
    print(fee_diag.to_string(index=False))
    
    # ETA brackets
    chk_merged["eta_bracket"] = pd.cut(
        chk_merged["eta_minutes"],
        bins=[0, 25, 39, 54, 200],
        labels=["1. Fast (< 25m)", "2. Standard (25-39m)", "3. Delayed (40-54m)", "4. Severe Delay (55m+)"]
    )
    eta_diag = chk_merged.groupby("eta_bracket", observed=False).agg(
        checkout_sessions=("session_id", "count"),
        orders_placed=("is_success", "sum")
    ).reset_index()
    eta_diag["conversion_pct"] = (eta_diag["orders_placed"] / eta_diag["checkout_sessions"] * 100).round(2)
    eta_diag["abandonment_pct"] = (100.0 - eta_diag["conversion_pct"]).round(2)
    print("\n[ETA Friction Diagnostic]")
    print(eta_diag.to_string(index=False))
    
    # Failure reasons breakdown
    fail_reasons = chk_merged[chk_merged["is_success"] == 0]["failure_reason"].value_counts().reset_index()
    fail_reasons.columns = ["failure_reason", "abandoned_count"]
    fail_reasons["pct_of_abandoned"] = (fail_reasons["abandoned_count"] / fail_reasons["abandoned_count"].sum() * 100).round(2)
    print("\n[Checkout Failure Reasons]")
    print(fail_reasons.to_string(index=False))
    
    fee_diag.to_csv("data/processed/dropoff_diagnostic.csv", index=False)
    print("\n[*] All summary datasets exported to data/processed/")

if __name__ == "__main__":
    run_analysis()

"""
Publication-Quality Visualization Generator
Author: Senior Product Analytics Engineer
Description: Generates high-resolution PNG charts illustrating the funnel drop-offs,
             cohort retention decay, ETA and fee elasticity, and A/B test modeling.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Configure theme & typography
sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
plt.rcParams["axes.edgecolor"] = "#E2E8F0"
plt.rcParams["axes.linewidth"] = 0.8

os.makedirs("images", exist_ok=True)

def generate_charts():
    print("[*] Generating publication-grade charts...")
    
    # ---------------------------------------------------------
    # Chart 1: Funnel Waterfall & Conversion Progression
    # ---------------------------------------------------------
    df_funnel = pd.read_csv("data/processed/funnel_summary.csv")
    
    fig, ax1 = plt.subplots(figsize=(11, 6), dpi=300)
    stages = [s.split(". ")[1] for s in df_funnel["stage_name"]]
    sessions = df_funnel["sessions"]
    cum_conv = df_funnel["cumulative_conversion_pct"]
    
    colors = ["#3B82F6", "#60A5FA", "#93C5FD", "#F59E0B", "#10B981"]
    bars = ax1.bar(stages, sessions, color=colors, width=0.55, edgecolor="#1E293B", linewidth=1.2, zorder=3)
    ax1.set_ylabel("Session Volume", fontsize=12, fontweight="bold", color="#1E293B")
    ax1.set_ylim(0, 48000)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}"))
    
    # Add volume & drop-off labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        step_drop = df_funnel.loc[i, "step_dropoff_pct"]
        step_conv = df_funnel.loc[i, "step_conversion_pct"]
        
        ax1.text(
            bar.get_x() + bar.get_width() / 2, 
            height + 800, 
            f"{int(height):,}", 
            ha="center", 
            va="bottom", 
            fontsize=11, 
            fontweight="bold", 
            color="#0F172A"
        )
        if i > 0:
            drop_color = "#DC2626" if step_drop > 50 else "#D97706"
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                height / 2,
                f"Drop: -{step_drop}%\n(Pass: {step_conv}%)",
                ha="center",
                va="center",
                fontsize=9.5,
                fontweight="bold",
                color="white",
                bbox=dict(boxstyle="round,pad=0.25", facecolor=drop_color, edgecolor="none", alpha=0.92)
            )
            
    # Highlight checkout bottleneck
    ax1.annotate(
        "CRITICAL BOTTLENECK:\n70.6% Drop-off at Checkout\n(10,098 High-Intent Sessions Lost)",
        xy=(3.5, 14298),
        xytext=(2.6, 28000),
        arrowprops=dict(facecolor="#DC2626", shrink=0.08, width=2.5, headwidth=9),
        fontsize=10.5,
        fontweight="bold",
        color="#DC2626",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEF2F2", edgecolor="#DC2626", linewidth=1.5)
    )
    
    plt.title("Food Delivery User Journey Funnel: App Open to Successful Order", fontsize=14, fontweight="bold", pad=20, color="#0F172A")
    plt.tight_layout()
    plt.savefig("images/01_funnel_waterfall.png")
    plt.close()
    print("[+] Saved images/01_funnel_waterfall.png")
    
    # ---------------------------------------------------------
    # Chart 2: Checkout Abandonment Root Causes
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    reasons = [
        "ETA Friction (>45m)",
        "Fee Shock Abandonment",
        "Price Comparison / Hesitation",
        "Payment Gateway Timeout",
        "Promo Restriction Barrier"
    ]
    counts = [3193, 2595, 1907, 1873, 530]
    pcts = [31.6, 25.7, 18.9, 18.6, 5.2]
    colors = ["#EF4444", "#F97316", "#FBBF24", "#6366F1", "#A855F7"]
    
    y_pos = np.arange(len(reasons))
    bars = ax.barh(y_pos, counts, color=colors, height=0.55, edgecolor="#0F172A", linewidth=1.1, zorder=3)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(reasons, fontsize=11, fontweight="medium", color="#1E293B")
    ax.invert_yaxis()
    ax.set_xlabel("Number of Abandoned Checkouts (Total: 10,098)", fontsize=11, fontweight="bold", color="#1E293B")
    ax.set_xlim(0, 3800)
    
    for bar, pct in zip(bars, pcts):
        width = bar.get_width()
        ax.text(width + 60, bar.get_y() + bar.get_height() / 2, f"{int(width):,} ({pct}%)", va="center", fontsize=10.5, fontweight="bold", color="#0F172A")
        
    plt.title("Root-Cause Breakdown: Why 10,098 Users Abandoned at Checkout", fontsize=13.5, fontweight="bold", pad=18, color="#0F172A")
    plt.tight_layout()
    plt.savefig("images/02_checkout_root_cause_drivers.png")
    plt.close()
    print("[+] Saved images/02_checkout_root_cause_drivers.png")
    
    # ---------------------------------------------------------
    # Chart 3: ETA Friction vs Checkout Abandonment Curve
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    eta_bins = ["Fast (<25m)", "Standard (25-39m)", "Delayed (40-54m)", "Severe Delay (55m+)"]
    conv_rates = [100.0, 35.03, 23.58, 14.24]
    abandon_rates = [0.0, 64.97, 76.42, 85.76]
    
    x = np.arange(len(eta_bins))
    ax.plot(x, conv_rates, marker="o", linewidth=3, markersize=8, color="#10B981", label="Checkout-to-Order Conversion %", zorder=4)
    ax.plot(x, abandon_rates, marker="s", linewidth=3, markersize=8, color="#EF4444", linestyle="--", label="Checkout Abandonment Rate %", zorder=4)
    
    ax.set_xticks(x)
    ax.set_xticklabels(eta_bins, fontsize=10.5, fontweight="bold", color="#1E293B")
    ax.set_ylabel("Rate (%)", fontsize=11, fontweight="bold", color="#1E293B")
    ax.set_ylim(-5, 115)
    ax.legend(frameon=True, facecolor="#F8FAFC", edgecolor="#E2E8F0", loc="center right", fontsize=10.5)
    
    for i, (c, a) in enumerate(zip(conv_rates, abandon_rates)):
        ax.text(i, c + 4, f"{c:.1f}%", ha="center", fontsize=10, fontweight="bold", color="#059669")
        if a > 0:
            ax.text(i, a - 7, f"{a:.1f}%", ha="center", fontsize=10, fontweight="bold", color="#DC2626")
            
    plt.title("Delivery ETA Sensitivity: Abandonment Escalation Beyond 40 Minutes", fontsize=13, fontweight="bold", pad=16, color="#0F172A")
    plt.tight_layout()
    plt.savefig("images/03_eta_fee_sensitivity.png")
    plt.close()
    print("[+] Saved images/03_eta_fee_sensitivity.png")
    
    # ---------------------------------------------------------
    # Chart 4: Discount Impact on Conversion & Re-order Velocity
    # ---------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
    
    # Left: Conversion Rate
    groups = ["No Discount", "Discount Applied"]
    conv_vals = [16.55, 48.60]
    bar_colors = ["#94A3B8", "#10B981"]
    b1 = ax1.bar(groups, conv_vals, color=bar_colors, width=0.45, edgecolor="#0F172A", linewidth=1.1)
    ax1.set_ylabel("Checkout Conversion Rate (%)", fontsize=11, fontweight="bold")
    ax1.set_ylim(0, 60)
    ax1.set_title("Checkout Conversion Lift with Promo", fontsize=12, fontweight="bold", pad=12)
    for bar in b1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, h + 1.2, f"{h:.1f}%", ha="center", fontweight="bold", fontsize=11)
        
    # Right: Days to Second Order
    reorder_labels = ["Organic 1st Order", "Promo 1st Order"]
    velocity_days = [38.90, 43.95]
    vel_colors = ["#3B82F6", "#F59E0B"]
    b2 = ax2.bar(reorder_labels, velocity_days, color=vel_colors, width=0.45, edgecolor="#0F172A", linewidth=1.1)
    ax2.set_ylabel("Average Days to 2nd Order", fontsize=11, fontweight="bold")
    ax2.set_ylim(0, 55)
    ax2.set_title("Re-order Velocity: The 'Promo Hangover'", fontsize=12, fontweight="bold", pad=12)
    for bar in b2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, h + 1.2, f"{h:.1f} days", ha="center", fontweight="bold", fontsize=11)
        
    plt.suptitle("The Dual Effect of Discounts: Higher Initial Conversion vs Slower Habit Formation", fontsize=13.5, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig("images/04_discount_impact_comparison.png")
    plt.close()
    print("[+] Saved images/04_discount_impact_comparison.png")
    
    # ---------------------------------------------------------
    # Chart 5: Cohort Retention Decay Heatmap
    # ---------------------------------------------------------
    df_cohort = pd.read_csv("data/processed/cohort_retention.csv")
    active_cohorts = df_cohort[df_cohort["cohort_month"] >= "2023-12"].copy()
    
    heatmap_data = active_cohorts.set_index("cohort_month")[[
        "d1_session_retention_pct", "d7_session_retention_pct", "d14_session_retention_pct", "d30_session_retention_pct"
    ]]
    heatmap_data.columns = ["Day 1", "Day 7", "Day 14", "Day 30"]
    
    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)
    sns.heatmap(
        heatmap_data, 
        annot=True, 
        fmt=".1f", 
        cmap="YlGnBu", 
        cbar_kws={'label': 'Retention Rate (%)'}, 
        linewidths=1.2, 
        linecolor="white",
        ax=ax
    )
    plt.title("Monthly User Cohort Retention Matrix (Active Sessions)", fontsize=13, fontweight="bold", pad=16, color="#0F172A")
    plt.ylabel("Signup Cohort Month", fontsize=11, fontweight="bold")
    plt.xlabel("Days Elapsed Since Signup", fontsize=11, fontweight="bold")
    plt.tight_layout()
    plt.savefig("images/05_cohort_retention_heatmap.png")
    plt.close()
    print("[+] Saved images/05_cohort_retention_heatmap.png")
    
    print("[*] All publication-grade visualizations generated successfully.")

if __name__ == "__main__":
    generate_charts()

/**
 * Food Delivery Product Funnel & Retention Analytics
 * Client-Side Controller & Chart Configuration
 * Theme: Simple, Clean Light Mode
 */

// Empirical Data Layer extracted from 41,176 sessions and 4,200 real transactions
const DATA_STORE = {
    overall: {
        total_sessions: 41176,
        s1_open: 41176,
        s2_discovery: 32426,
        s3_add_to_cart: 19381,
        s4_checkout: 14298,
        s5_order_success: 4200,
        conv_rate: 10.20,
        checkout_dropoff: 70.63,
        repeat_buyer_rate: 99.8,
        d30_retention: 45.83
    },
    funnel_stages: [
        { step: 1, name: "1. App Open", sessions: 41176, step_conv: 100.0, step_drop: 0.0, cum_conv: 100.0, color: "#1E293B" },
        { step: 2, name: "2. Restaurant Discovery", sessions: 32426, step_conv: 78.75, step_drop: 21.25, cum_conv: 78.75, color: "#334155" },
        { step: 3, name: "3. Add to Cart", sessions: 19381, step_conv: 59.77, step_drop: 40.23, cum_conv: 47.07, color: "#475569" },
        { step: 4, name: "4. Initiate Checkout", sessions: 14298, step_conv: 73.77, step_drop: 26.23, cum_conv: 34.72, color: "#DC2626" },
        { step: 5, name: "5. Successful Order", sessions: 4200, step_conv: 29.37, step_drop: 70.63, cum_conv: 10.20, color: "#16A34A" }
    ],
    platforms: {
        "iOS": { sessions: 22202, checkout_conv: 29.78, end_conv: 10.32 },
        "Android": { sessions: 14344, checkout_conv: 28.65, end_conv: 9.96 },
        "Web": { sessions: 4630, checkout_conv: 29.70, end_conv: 10.35 }
    },
    cities: {
        "Mumbai": { sessions: 13164, checkout_conv: 29.30, end_conv: 10.13 },
        "Bengaluru": { sessions: 10404, checkout_conv: 28.73, end_conv: 10.07 },
        "Delhi NCR": { sessions: 8513, checkout_conv: 30.39, end_conv: 10.60 },
        "Hyderabad": { sessions: 5078, checkout_conv: 29.31, end_conv: 10.14 },
        "Pune": { sessions: 4017, checkout_conv: 29.24, end_conv: 10.01 }
    },
    discounts: {
        "Discount Applied": { sessions: 13605, checkout_conv: 48.60, end_conv: 20.44 },
        "No Discount": { sessions: 27571, checkout_conv: 16.55, end_conv: 5.15 }
    },
    eta_bins: [
        { label: "< 25m", conv: 100.0, drop: 0.0, volume: 616 },
        { label: "25–39m", conv: 35.03, drop: 64.97, volume: 5010 },
        { label: "40–54m", conv: 23.58, drop: 76.42, volume: 6361 },
        { label: "55m+", conv: 14.24, drop: 85.76, volume: 2311 }
    ],
    failure_reasons: [
        { reason: "ETA Delay (>40m)", count: 3193, pct: 31.62, color: "#DC2626" },
        { reason: "Fee Surcharges", count: 2595, pct: 25.70, color: "#D97706" },
        { reason: "Price Comparison / Hesitation", count: 1907, pct: 18.88, color: "#475569" },
        { reason: "Payment Gateway Timeout", count: 1873, pct: 18.55, color: "#1E3A8A" },
        { reason: "Promo Restriction Barrier", count: 530, pct: 5.25, color: "#94A3B8" }
    ],
    reorder_velocity: [
        { type: "Organic 1st Order", avg_days: 38.90, median_days: 23.76, repeat_users: 179 },
        { type: "Promo 1st Order", avg_days: 43.95, median_days: 29.97, repeat_users: 320 }
    ]
};

// Global Chart References
let chartFunnelWaterfallInstance = null;
let chartPlatformFunnelInstance = null;
let chartCityFunnelInstance = null;
let chartDiscountFunnelInstance = null;
let chartEtaSensitivityInstance = null;
let chartFailureReasonsInstance = null;
let chartReorderVelocityInstance = null;

// Initialize on DOM Load
document.addEventListener("DOMContentLoaded", () => {
    renderFunnelTable();
    initCharts();
    updateSimulator();
});

// Render the stage table
function renderFunnelTable() {
    const tbody = document.getElementById("funnelTableBody");
    if (!tbody) return;
    
    tbody.innerHTML = "";
    DATA_STORE.funnel_stages.forEach((stage) => {
        const tr = document.createElement("tr");
        const dropText = stage.step_drop > 50 
            ? `<span style="color: #DC2626; font-weight: 600;">-${stage.step_drop}% (Bottleneck)</span>`
            : (stage.step_drop > 0 ? `-${stage.step_drop}%` : `0.0%`);
            
        tr.innerHTML = `
            <td><strong>${stage.name}</strong></td>
            <td>${stage.sessions.toLocaleString()}</td>
            <td>${stage.step_conv}%</td>
            <td>${dropText}</td>
            <td><strong>${stage.cum_conv}%</strong></td>
        `;
        tbody.appendChild(tr);
    });
}

// Chart Font & Grid Defaults for Clean Light Mode
Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = "#4B5563";

// Initialize Simple Clean Charts
function initCharts() {
    // 1. Funnel Progression Chart
    const ctxFunnel = document.getElementById("chartFunnelWaterfall");
    if (ctxFunnel) {
        chartFunnelWaterfallInstance = new Chart(ctxFunnel, {
            type: "bar",
            data: {
                labels: DATA_STORE.funnel_stages.map(s => s.name.split(". ")[1]),
                datasets: [{
                    label: "Sessions Reached",
                    data: DATA_STORE.funnel_stages.map(s => s.sessions),
                    backgroundColor: DATA_STORE.funnel_stages.map(s => s.color),
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const idx = context.dataIndex;
                                const stage = DATA_STORE.funnel_stages[idx];
                                return [
                                    `Sessions: ${stage.sessions.toLocaleString()}`,
                                    `Step Pass Rate: ${stage.step_conv}%`,
                                    `Step Drop-off: -${stage.step_drop}%`,
                                    `Cumulative Conv: ${stage.cum_conv}%`
                                ];
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        grid: { color: "#F3F4F6" },
                        ticks: { color: "#6B7280" }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: "#111827", font: { weight: "600" } }
                    }
                }
            }
        });
    }

    // 2. Platform Comparison Chart
    const ctxPlat = document.getElementById("chartPlatformFunnel");
    if (ctxPlat) {
        chartPlatformFunnelInstance = new Chart(ctxPlat, {
            type: "bar",
            data: {
                labels: Object.keys(DATA_STORE.platforms),
                datasets: [{
                    label: "Checkout Conversion (%)",
                    data: Object.values(DATA_STORE.platforms).map(p => p.checkout_conv),
                    backgroundColor: "#1E293B",
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { max: 40, ticks: { callback: v => v + "%", color: "#6B7280" }, grid: { color: "#F3F4F6" } },
                    x: { ticks: { color: "#111827", font: { weight: "500" } }, grid: { display: false } }
                }
            }
        });
    }

    // 3. City Funnel Comparison
    const ctxCity = document.getElementById("chartCityFunnel");
    if (ctxCity) {
        chartCityFunnelInstance = new Chart(ctxCity, {
            type: "bar",
            data: {
                labels: Object.keys(DATA_STORE.cities),
                datasets: [{
                    label: "Checkout Conv (%)",
                    data: Object.values(DATA_STORE.cities).map(c => c.checkout_conv),
                    backgroundColor: "#334155",
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: { legend: { display: false } },
                scales: {
                    x: { max: 40, ticks: { callback: v => v + "%", color: "#6B7280" }, grid: { color: "#F3F4F6" } },
                    y: { ticks: { color: "#111827" }, grid: { display: false } }
                }
            }
        });
    }

    // 4. Discount Funnel Comparison
    const ctxDisc = document.getElementById("chartDiscountFunnel");
    if (ctxDisc) {
        chartDiscountFunnelInstance = new Chart(ctxDisc, {
            type: "bar",
            data: {
                labels: ["Organic (No Promo)", "Discount Applied"],
                datasets: [{
                    label: "Checkout Conv (%)",
                    data: [DATA_STORE.discounts["No Discount"].checkout_conv, DATA_STORE.discounts["Discount Applied"].checkout_conv],
                    backgroundColor: ["#94A3B8", "#1E293B"],
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { max: 60, ticks: { callback: v => v + "%", color: "#6B7280" }, grid: { color: "#F3F4F6" } },
                    x: { ticks: { color: "#111827", font: { weight: "500" } }, grid: { display: false } }
                }
            }
        });
    }

    // 5. ETA Sensitivity Curve
    const ctxEta = document.getElementById("chartEtaSensitivity");
    if (ctxEta) {
        chartEtaSensitivityInstance = new Chart(ctxEta, {
            type: "line",
            data: {
                labels: DATA_STORE.eta_bins.map(e => e.label),
                datasets: [
                    {
                        label: "Checkout Conversion Rate (%)",
                        data: DATA_STORE.eta_bins.map(e => e.conv),
                        borderColor: "#16A34A",
                        backgroundColor: "#16A34A",
                        fill: false,
                        tension: 0.2,
                        pointRadius: 4
                    },
                    {
                        label: "Checkout Abandonment Rate (%)",
                        data: DATA_STORE.eta_bins.map(e => e.drop),
                        borderColor: "#DC2626",
                        backgroundColor: "#DC2626",
                        borderDash: [4, 4],
                        fill: false,
                        tension: 0.2,
                        pointRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: "#374151" } }
                },
                scales: {
                    y: { max: 105, ticks: { callback: v => v + "%", color: "#6B7280" }, grid: { color: "#F3F4F6" } },
                    x: { ticks: { color: "#111827", font: { weight: "500" } }, grid: { display: false } }
                }
            }
        });
    }

    // 6. Checkout Failure Reasons (Donut)
    const ctxFail = document.getElementById("chartFailureReasons");
    if (ctxFail) {
        chartFailureReasonsInstance = new Chart(ctxFail, {
            type: "doughnut",
            data: {
                labels: DATA_STORE.failure_reasons.map(f => f.reason),
                datasets: [{
                    data: DATA_STORE.failure_reasons.map(f => f.count),
                    backgroundColor: DATA_STORE.failure_reasons.map(f => f.color),
                    borderWidth: 1,
                    borderColor: "#FFFFFF"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "right", labels: { color: "#374151", font: { size: 11.5 } } },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const idx = context.dataIndex;
                                const item = DATA_STORE.failure_reasons[idx];
                                return `${item.reason}: ${item.count.toLocaleString()} (${item.pct}%)`;
                            }
                        }
                    }
                },
                cutout: "65%"
            }
        });
    }

    // 7. Re-order Velocity Chart
    const ctxVel = document.getElementById("chartReorderVelocity");
    if (ctxVel) {
        chartReorderVelocityInstance = new Chart(ctxVel, {
            type: "bar",
            data: {
                labels: DATA_STORE.reorder_velocity.map(v => v.type),
                datasets: [
                    {
                        label: "Average Days to 2nd Order",
                        data: DATA_STORE.reorder_velocity.map(v => v.avg_days),
                        backgroundColor: ["#1E293B", "#64748B"],
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: ctx => `Avg Days to 2nd Order: ${ctx.parsed.y} days`
                        }
                    }
                },
                scales: {
                    y: { max: 55, ticks: { callback: v => v + " d", color: "#6B7280" }, grid: { color: "#F3F4F6" } },
                    x: { ticks: { color: "#111827", font: { weight: "500" } }, grid: { display: false } }
                }
            }
        });
    }
}

// Global Filter Interactivity
function applyGlobalFilters() {
    const plat = document.getElementById("filterPlatform").value;
    const disc = document.getElementById("filterDiscount").value;

    let baseSessions = DATA_STORE.overall.total_sessions;
    let baseConv = DATA_STORE.overall.conv_rate;
    let baseDrop = DATA_STORE.overall.checkout_dropoff;
    let baseOrders = DATA_STORE.overall.s5_order_success;

    // Platform slice adjustment
    if (plat !== "All" && DATA_STORE.platforms[plat]) {
        baseSessions = DATA_STORE.platforms[plat].sessions;
        baseConv = DATA_STORE.platforms[plat].end_conv;
        baseDrop = (100.0 - DATA_STORE.platforms[plat].checkout_conv).toFixed(2);
        baseOrders = Math.round(baseSessions * (baseConv / 100));
    }

    // Discount slice adjustment
    if (disc !== "All" && DATA_STORE.discounts[disc]) {
        baseSessions = DATA_STORE.discounts[disc].sessions;
        baseConv = DATA_STORE.discounts[disc].end_conv;
        baseDrop = (100.0 - DATA_STORE.discounts[disc].checkout_conv).toFixed(2);
        baseOrders = Math.round(baseSessions * (baseConv / 100));
    }

    // Update KPI cards
    document.getElementById("kpiSessions").textContent = baseSessions.toLocaleString();
    document.getElementById("kpiConvRate").textContent = baseConv + "%";
    document.getElementById("kpiDropoff").textContent = baseDrop + "%";
    document.getElementById("kpiOrders").textContent = baseOrders.toLocaleString();
}

function resetFilters() {
    document.getElementById("filterPlatform").value = "All";
    document.getElementById("filterCity").value = "All";
    document.getElementById("filterSegment").value = "All";
    document.getElementById("filterDiscount").value = "All";
    applyGlobalFilters();
}

// Tab Switching
function switchTab(tabId) {
    document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
    document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));

    const activeBtn = document.getElementById(`tab${tabId.charAt(0).toUpperCase() + tabId.slice(1)}`);
    const activePane = document.getElementById(`pane-${tabId}`);

    if (activeBtn) activeBtn.classList.add("active");
    if (activePane) activePane.classList.add("active");
}

// Interactive A/B Experiment Calculator
function updateSimulator() {
    const lift = parseFloat(document.getElementById("sliderLift").value);
    const aov = parseFloat(document.getElementById("sliderAov").value);
    const traffic = parseInt(document.getElementById("sliderTraffic").value);

    document.getElementById("valLift").textContent = `+${lift.toFixed(1)}%`;
    document.getElementById("valAov").textContent = `₹${aov}`;
    document.getElementById("valTraffic").textContent = traffic.toLocaleString();

    const baselineConv = 29.37;
    const newConv = baselineConv + lift;

    const incOrders = Math.round(traffic * (lift / 100));
    const incMonthlyGmv = Math.round(incOrders * aov);
    const annualGmv = incMonthlyGmv * 12;

    document.getElementById("resNewConv").textContent = `${newConv.toFixed(2)}%`;
    document.getElementById("resIncOrders").textContent = `+${incOrders.toLocaleString()} Orders`;
    document.getElementById("resIncGmv").textContent = `₹${incMonthlyGmv.toLocaleString()}`;
    document.getElementById("resAnnualGmv").textContent = `₹${annualGmv.toLocaleString()}`;
}

// Clipboard Helper
function copyCode(elementId) {
    const codeEl = document.getElementById(elementId);
    if (!codeEl) return;
    navigator.clipboard.writeText(codeEl.innerText).then(() => {
        alert("SQL / DAX snippet copied to clipboard.");
    });
}

// CSV Export
function exportSummaryData() {
    const csvContent = "data:text/csv;charset=utf-8," + 
        "Step,Stage Name,Sessions Reached,Step Conversion %,Step Drop-off %,Cumulative Conversion %\n" +
        DATA_STORE.funnel_stages.map(s => `${s.step},"${s.name}",${s.sessions},${s.step_conv},${s.step_drop},${s.cum_conv}`).join("\n");
        
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "food_delivery_funnel_summary.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

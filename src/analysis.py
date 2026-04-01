"""
analysis.py
Supply Chain Operations Analytics Pipeline
Computes KPIs, identifies bottlenecks, and generates structured insights.
"""
import pandas as pd
import numpy as np
import json
import os

# ── Load Data ─────────────────────────────────────────────────────────────────
orders = pd.read_csv("data/orders.csv", parse_dates=["order_date", "delivery_date"])
inventory = pd.read_csv("data/inventory.csv")

print("=" * 60)
print("SUPPLY CHAIN OPERATIONS ANALYTICS PIPELINE")
print("=" * 60)

# ── KPI 1: On-Time Delivery Rate ──────────────────────────────────────────────
overall_otd = orders["is_on_time"].mean() * 100
otd_by_supplier = orders.groupby("supplier")["is_on_time"].mean().mul(100).round(2).reset_index()
otd_by_supplier.columns = ["supplier", "on_time_delivery_pct"]
otd_by_supplier["status"] = otd_by_supplier["on_time_delivery_pct"].apply(
    lambda x: "CRITICAL" if x < 70 else ("AT RISK" if x < 85 else "HEALTHY")
)
otd_by_supplier = otd_by_supplier.sort_values("on_time_delivery_pct")

print(f"\n[KPI 1] Overall On-Time Delivery Rate: {overall_otd:.1f}%")
print(otd_by_supplier.to_string(index=False))

# ── KPI 2: Average Delay by Carrier ──────────────────────────────────────────
delay_by_carrier = orders[orders["delay_days"] > 0].groupby("carrier").agg(
    avg_delay_days=("delay_days", "mean"),
    total_delayed_orders=("order_id", "count")
).round(2).reset_index().sort_values("avg_delay_days", ascending=False)

print(f"\n[KPI 2] Average Delay by Carrier (delayed orders only):")
print(delay_by_carrier.to_string(index=False))

# ── KPI 3: Delay Root Cause Analysis ─────────────────────────────────────────
delay_reasons = orders[orders["delay_reason"] != "None"]["delay_reason"].value_counts().reset_index()
delay_reasons.columns = ["delay_reason", "count"]
delay_reasons["pct"] = (delay_reasons["count"] / delay_reasons["count"].sum() * 100).round(1)

print(f"\n[KPI 3] Delay Root Cause Analysis:")
print(delay_reasons.to_string(index=False))

# ── KPI 4: Supplier Performance Scorecard ────────────────────────────────────
supplier_scorecard = orders.groupby("supplier").agg(
    total_orders=("order_id", "count"),
    on_time_pct=("is_on_time", lambda x: round(x.mean() * 100, 1)),
    avg_delay_days=("delay_days", "mean"),
    total_spend=("total_cost", "sum")
).round(2).reset_index()
supplier_scorecard["total_spend"] = supplier_scorecard["total_spend"].apply(lambda x: f"€{x:,.0f}")
supplier_scorecard["risk_rating"] = supplier_scorecard["on_time_pct"].apply(
    lambda x: "CRITICAL" if x < 70 else ("AT RISK" if x < 85 else "HEALTHY")
)

print(f"\n[KPI 4] Supplier Performance Scorecard:")
print(supplier_scorecard.to_string(index=False))

# ── KPI 5: Monthly Shipment Volume Trend ─────────────────────────────────────
orders["month"] = orders["order_date"].dt.month
monthly_volume = orders.groupby("month").agg(
    shipments=("order_id", "count"),
    on_time_pct=("is_on_time", lambda x: round(x.mean() * 100, 1)),
    total_spend=("total_cost", "sum")
).round(2).reset_index()

print(f"\n[KPI 5] Monthly Shipment Volume:")
print(monthly_volume.to_string(index=False))

# ── KPI 6: Inventory Stockout Risk ───────────────────────────────────────────
stockout_risk = inventory[inventory["stockout_risk"]].groupby(["warehouse", "product_category"]).size().reset_index(name="months_at_risk")
stockout_risk = stockout_risk.sort_values("months_at_risk", ascending=False)

print(f"\n[KPI 6] Stockout Risk by Warehouse and Category (months below safety threshold):")
print(stockout_risk.head(10).to_string(index=False))

# ── KPI 7: Warehouse Inbound Volume ──────────────────────────────────────────
warehouse_volume = orders.groupby("warehouse").agg(
    total_orders=("order_id", "count"),
    total_units=("quantity", "sum"),
    on_time_pct=("is_on_time", lambda x: round(x.mean() * 100, 1))
).reset_index().sort_values("total_orders", ascending=False)

print(f"\n[KPI 7] Warehouse Inbound Volume:")
print(warehouse_volume.to_string(index=False))

# ── Save Outputs ──────────────────────────────────────────────────────────────
os.makedirs("reports", exist_ok=True)
otd_by_supplier.to_csv("reports/supplier_otd_scorecard.csv", index=False)
delay_by_carrier.to_csv("reports/carrier_delay_analysis.csv", index=False)
delay_reasons.to_csv("reports/delay_root_causes.csv", index=False)
supplier_scorecard.to_csv("reports/supplier_performance_scorecard.csv", index=False)
monthly_volume.to_csv("reports/monthly_shipment_trends.csv", index=False)
stockout_risk.to_csv("reports/inventory_stockout_risk.csv", index=False)
warehouse_volume.to_csv("reports/warehouse_volume.csv", index=False)

# ── Summary JSON for dashboard ────────────────────────────────────────────────
summary = {
    "total_orders": len(orders),
    "overall_otd_pct": round(overall_otd, 1),
    "critical_suppliers": otd_by_supplier[otd_by_supplier["status"] == "CRITICAL"]["supplier"].tolist(),
    "top_delay_reason": delay_reasons.iloc[0]["delay_reason"] if len(delay_reasons) > 0 else "None",
    "stockout_risk_count": len(stockout_risk),
    "total_spend": f"€{orders['total_cost'].sum():,.0f}"
}
with open("reports/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\n[OUTPUT] All reports saved to /reports/")
print(f"[SUMMARY] {json.dumps(summary, indent=2)}")

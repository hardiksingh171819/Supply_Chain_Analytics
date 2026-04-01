"""
generate_data.py
Generates synthetic supply chain operations data for analysis.
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

np.random.seed(42)
random.seed(42)

SUPPLIERS = ["SupplierA", "SupplierB", "SupplierC", "SupplierD", "SupplierE"]
WAREHOUSES = ["Amsterdam", "Rotterdam", "Brussels", "Paris", "Frankfurt"]
PRODUCT_CATEGORIES = ["Kitchen Appliances", "Coffee Machines", "Air Purifiers", "Irons", "Blenders"]
CARRIERS = ["DHL", "FedEx", "UPS", "DSV", "DB Schenker"]
DELAY_REASONS = ["Customs clearance", "Carrier delay", "Warehouse capacity", "Bad weather", "None", "None", "None", "None"]

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

# ── Orders ────────────────────────────────────────────────────────────────────
n_orders = 500
order_ids = [f"ORD-{str(i).zfill(4)}" for i in range(1, n_orders + 1)]
order_dates = [random_date(start_date, end_date) for _ in range(n_orders)]
promised_days = np.random.choice([3, 5, 7, 10], n_orders, p=[0.2, 0.4, 0.3, 0.1])
actual_days = promised_days + np.random.choice([-1, 0, 0, 0, 1, 2, 3, 5], n_orders, p=[0.05, 0.35, 0.2, 0.1, 0.1, 0.1, 0.07, 0.03])
actual_days = np.clip(actual_days, 1, 20)

orders_df = pd.DataFrame({
    "order_id": order_ids,
    "order_date": order_dates,
    "supplier": np.random.choice(SUPPLIERS, n_orders),
    "warehouse": np.random.choice(WAREHOUSES, n_orders),
    "product_category": np.random.choice(PRODUCT_CATEGORIES, n_orders),
    "carrier": np.random.choice(CARRIERS, n_orders),
    "quantity": np.random.randint(10, 500, n_orders),
    "unit_cost": np.round(np.random.uniform(15, 250, n_orders), 2),
    "promised_delivery_days": promised_days,
    "actual_delivery_days": actual_days,
    "delay_reason": [random.choice(DELAY_REASONS) if actual_days[i] > promised_days[i] else "None" for i in range(n_orders)]
})

orders_df["delivery_date"] = [
    orders_df["order_date"].iloc[i] + timedelta(days=int(orders_df["actual_delivery_days"].iloc[i]))
    for i in range(n_orders)
]
orders_df["is_on_time"] = orders_df["actual_delivery_days"] <= orders_df["promised_delivery_days"]
orders_df["total_cost"] = orders_df["quantity"] * orders_df["unit_cost"]
orders_df["delay_days"] = (orders_df["actual_delivery_days"] - orders_df["promised_delivery_days"]).clip(lower=0)

# ── Inventory ─────────────────────────────────────────────────────────────────
inventory_records = []
for warehouse in WAREHOUSES:
    for category in PRODUCT_CATEGORIES:
        for month in range(1, 13):
            inventory_records.append({
                "warehouse": warehouse,
                "product_category": category,
                "month": month,
                "opening_stock": random.randint(100, 2000),
                "units_received": random.randint(50, 500),
                "units_sold": random.randint(40, 450),
                "safety_stock_threshold": 150
            })

inventory_df = pd.DataFrame(inventory_records)
inventory_df["closing_stock"] = (inventory_df["opening_stock"] + inventory_df["units_received"] - inventory_df["units_sold"]).clip(lower=0)
inventory_df["stockout_risk"] = inventory_df["closing_stock"] < inventory_df["safety_stock_threshold"]

os.makedirs("data", exist_ok=True)
orders_df.to_csv("data/orders.csv", index=False)
inventory_df.to_csv("data/inventory.csv", index=False)
print(f"Generated {len(orders_df)} orders and {len(inventory_df)} inventory records.")

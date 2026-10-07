import sqlite3
import pandas as pd
from statistics import NormalDist

# --- Assumptions (change these to test scenarios) ---
SERVICE_LEVEL = 0.95   # want enough stock 95% of the time
TARGET_MONTHS = 3      # months of demand to keep in stock

z = NormalDist().inv_cdf(SERVICE_LEVEL)   # about 1.645

conn = sqlite3.connect("data/nike_inventory.db")
products = pd.read_sql("SELECT * FROM products", conn)
sales = pd.read_sql("SELECT * FROM monthly_sales", conn)
conn.close()

# 1. Average demand and variability over the last 12 months
recent = sales[sales["month"] >= "2025-10"]
stats = (recent.groupby("sku")["units_sold"]
         .agg(avg_demand="mean", demand_std="std")
         .reset_index())

# 2. Trend: last 3 months vs. the 3 months before
last_3 = sales[sales["month"] >= "2026-07"].groupby("sku")["units_sold"].mean().rename("last_3")
prior_3 = (sales[(sales["month"] >= "2026-04") & (sales["month"] < "2026-07")]
           .groupby("sku")["units_sold"].mean().rename("prior_3"))

df = products.merge(stats, on="sku").merge(last_3, on="sku").merge(prior_3, on="sku")
df["trend"] = (df["last_3"] / df["prior_3"]).clip(0.8, 1.2)

# 3. Forecast, safety stock, target, and order quantity
df["forecast_monthly"] = df["avg_demand"] * df["trend"]
df["safety_stock"] = z * df["demand_std"] * df["lead_time_months"] ** 0.5
df["target_stock"] = df["forecast_monthly"] * TARGET_MONTHS + df["safety_stock"]
df["order_qty"] = (df["target_stock"] - df["on_hand"] - df["on_order"]).clip(lower=0).round(-2)
df["order_value"] = df["order_qty"] * df["unit_cost"]

# 4. Show the plan
cols = ["product_name", "trend", "forecast_monthly", "safety_stock",
        "on_hand", "on_order", "order_qty", "order_value"]
plan = df[cols].sort_values("order_value", ascending=False)
print(plan.round(2).to_string(index=False))
print()
print(f"Products to reorder: {(df['order_qty'] > 0).sum()} of {len(df)}")
print(f"Total order value at cost: ${df['order_value'].sum():,.0f}")

# 5. Save the plan for the Excel report later
plan.to_csv("output/reorder_plan.csv", index=False)
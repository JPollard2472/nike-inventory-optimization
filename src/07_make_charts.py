import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

conn = sqlite3.connect("data/nike_inventory.db")
with open("sql/02_inventory_status.sql") as f:
    status = pd.read_sql(f.read(), conn)
conn.close()

# Chart 1: months of supply for every product, colored by status
colors = {"Overstocked": "#d1495b", "Healthy": "#8d99ae", "At Risk": "#edae49"}
data = status.sort_values("months_of_supply")
fig, ax = plt.subplots(figsize=(9, 7))
ax.barh(data["product_name"], data["months_of_supply"],
        color=data["status"].map(colors))
ax.axvline(4, color="#d1495b", linestyle="--", linewidth=1)
ax.axvline(1.5, color="#edae49", linestyle="--", linewidth=1)
ax.set_xlabel("Months of supply on hand")
ax.set_title("Months of Supply by Product (dashed lines = thresholds)")
ax.legend(handles=[Patch(color=c, label=n) for n, c in colors.items()],
          loc="lower right")
plt.tight_layout()
plt.savefig("output/months_of_supply.png", dpi=150)
plt.close()

# Chart 2: dollars of excess inventory in the overstocked products
excess = status[status["excess_value_usd"] > 0].sort_values("excess_value_usd")
fig, ax = plt.subplots(figsize=(9, 4))
ax.barh(excess["product_name"], excess["excess_value_usd"] / 1_000_000, color="#d1495b")
ax.set_xlabel("Excess inventory at cost ($ millions)")
ax.set_title(f"${excess['excess_value_usd'].sum() / 1_000_000:.1f}M of Excess Inventory in 5 Products")
plt.tight_layout()
plt.savefig("output/excess_inventory.png", dpi=150)
plt.close()

print("Charts saved to output/")
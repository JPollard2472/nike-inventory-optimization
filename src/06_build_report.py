import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nike_inventory.db")

def run_sql(path):
    with open(path) as f:
        return pd.read_sql(f.read(), conn)

status = run_sql("sql/02_inventory_status.sql")
abc = run_sql("sql/03_abc_analysis.sql")
conn.close()
reorder = pd.read_csv("output/reorder_plan.csv")

summary = pd.DataFrame({
    "Metric": [
        "Products analyzed",
        "Overstocked products",
        "At-risk products",
        "Excess inventory at cost ($)",
        "Products to reorder",
        "Recommended order value ($)",
    ],
    "Value": [
        len(status),
        (status["status"] == "Overstocked").sum(),
        (status["status"] == "At Risk").sum(),
        round(status["excess_value_usd"].sum()),
        (reorder["order_qty"] > 0).sum(),
        round(reorder["order_value"].sum()),
    ],
})

with pd.ExcelWriter("output/nike_inventory_report.xlsx") as writer:
    summary.to_excel(writer, sheet_name="Summary", index=False)
    status.to_excel(writer, sheet_name="Inventory Status", index=False)
    abc.to_excel(writer, sheet_name="ABC Analysis", index=False)
    reorder.to_excel(writer, sheet_name="Reorder Plan", index=False)

print(summary.to_string(index=False))
print()
print("Report saved: output/nike_inventory_report.xlsx")
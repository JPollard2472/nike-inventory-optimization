import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nike_inventory.db")

with open("sql/02_inventory_status.sql") as f:
    query = f.read()

result = pd.read_sql(query, conn)
print(result.to_string(index=False))
print()
print(f"Total excess inventory at cost: ${result['excess_value_usd'].sum():,.0f}")

conn.close()
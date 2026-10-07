import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nike_inventory.db")

with open("sql/01_months_of_supply.sql") as f:
    query = f.read()

result = pd.read_sql(query, conn)
print(result.to_string(index=False))

conn.close()
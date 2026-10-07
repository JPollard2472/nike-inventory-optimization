import sqlite3
import pandas as pd

# Read the CSV files
products = pd.read_csv("data/products.csv")
sales = pd.read_csv("data/monthly_sales.csv")

# Create the database and load each file as a table
conn = sqlite3.connect("data/nike_inventory.db")
products.to_sql("products", conn, if_exists="replace", index=False)
sales.to_sql("monthly_sales", conn, if_exists="replace", index=False)

# Check that it worked
print(pd.read_sql("SELECT COUNT(*) AS products FROM products", conn))
print(pd.read_sql("SELECT COUNT(*) AS sales_rows FROM monthly_sales", conn))

conn.close()
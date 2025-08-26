import pandas as pd
import sqlite3

# Load CSVs
dfs = {name: pd.read_csv(f"data/{name}.csv") for name in ["products", "customers", "regions", "sales"]}

conn = sqlite3.connect("data/sales_dw.db")

# Insert data into SQLite
dfs["products"].to_sql("Product", conn, if_exists="append", index=False)
dfs["customers"].to_sql("Customer", conn, if_exists="append", index=False)
dfs["regions"].to_sql("Region", conn, if_exists="append", index=False)
dfs["sales"].to_sql("Sales", conn, if_exists="append", index=False)

# Merge tables for analysis
df = pd.read_sql("""
SELECT s.sale_id, s.date, s.sales_amount,
       c.name AS customer, c.age, c.gender,
       p.product_name, p.category,
       r.region_name
FROM Sales s
JOIN Customer c ON s.customer_id = c.customer_id
JOIN Product p ON s.product_id = p.product_id
JOIN Region r ON s.region_id = r.region_id
""", conn)

conn.close()

# Wrangling
df["sales_amount"].fillna(df["sales_amount"].median(), inplace=True)
df.dropna(subset=["customer"], inplace=True)
df.rename(columns={"sales_amount": "amount_usd"}, inplace=True)
df["date"] = pd.to_datetime(df["date"])
df["high_value_sale"] = df["amount_usd"] > 1000
df["month"] = df["date"].dt.to_period("M")
df["year"] = df["date"].dt.to_period("Y")

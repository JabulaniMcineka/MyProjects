import sqlite3

conn = sqlite3.connect("sales_dw.db")
cur = conn.cursor()

# Drop existing tables
cur.execute("DROP TABLE IF EXISTS Sales")
cur.execute("DROP TABLE IF EXISTS Product")
cur.execute("DROP TABLE IF EXISTS Customer")
cur.execute("DROP TABLE IF EXISTS Region")

# Create tables
cur.execute("""
CREATE TABLE Product (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT
)
""")

cur.execute("""
CREATE TABLE Customer (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT
)
""")

cur.execute("""
CREATE TABLE Region (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT
)
""")

cur.execute("""
CREATE TABLE Sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    customer_id INTEGER,
    region_id INTEGER,
    date TEXT,
    sales_amount REAL,
    FOREIGN KEY(product_id) REFERENCES Product(product_id),
    FOREIGN KEY(customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY(region_id) REFERENCES Region(region_id)
)
""")

conn.commit()
conn.close()
print("Data warehouse created successfully!")

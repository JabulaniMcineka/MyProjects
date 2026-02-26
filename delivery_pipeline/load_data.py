import sqlite3
import csv

cursor.execute("DROP TABLE IF EXISTS delevery;")

# Connect to SQLite database
conn = sqlite3.connect("deliveries.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS delivery (
    delivery_id TEXT PRIMARY KEY,
    city TEXT,
    customer_id INTEGER,
    scheduled_datetime TEXT,
    delivered_datetime TEXT,
    status TEXT,
    delay_minutes INTEGER,
    carrier TEXT,
    distance_km REAL,
    weight_kg REAL
)
""")



# FULL Windows path (use raw string r"")
file_path = r"C:\MyProjects\delivery_pipeline\Data\delivery_data.csv"

with open(file_path, newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute("""
        INSERT INTO delivery VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["delivery_id"],
            row["city"],
            row["customer_id"],
            row["scheduled_datetime"],
            row["delivered_datetime"],
            row["status"],
            row["delay_minutes"],
            row["carrier"],
            row["distance_km"],
            row["weight_kg"]
        ))

conn.commit()
conn.close()

print("Data successf" \
"ully loaded.")
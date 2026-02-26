import sqlite3

conn = sqlite3.connect("deliveries.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = OFF;")

#Drop tables in correct order (fact first)
cursor.execute("DROP TABLE IF EXISTS deliveries;")
cursor.execute("DROP TABLE IF EXISTS cities;")
cursor.execute("DROP TABLE IF EXISTS carriers;")
cursor.execute("DROP TABLE IF EXISTS customer")

cursor.execute("PRAGMA foreign_keys = ON;")

#Create Cities table
cursor.execute("""
CREATE TABLE cities (
    city_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT UNIQUE
);
""")

cursor.execute("""
INSERT INTO cities (city_name)
SELECT DISTINCT city
FROM delivery;
""")

#Create Carriers table
cursor.execute("""
CREATE TABLE carriers (
    carrier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    carrier_name TEXT UNIQUE
);
""")

cursor.execute("""
INSERT INTO carriers (carrier_name)
SELECT DISTINCT carrier
FROM delivery;
""")

#Create Deliveries fact table
cursor.execute("""
CREATE TABLE deliveries (
    delivery_id TEXT PRIMARY KEY,
    customer_id INTEGER,
    city_id INTEGER,
    carrier_id INTEGER,
    scheduled_datetime TEXT,
    delivered_datetime TEXT,
    status TEXT,
    delay_minutes INTEGER,
    distance_km REAL,
    weight_kg REAL,
    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    FOREIGN KEY (carrier_id) REFERENCES carriers(carrier_id)
);
""")

#Populate fact table
cursor.execute("""
INSERT INTO deliveries
SELECT 
    d.delivery_id,
    d.customer_id,
    c.city_id,
    cr.carrier_id,
    d.scheduled_datetime,
    d.delivered_datetime,
    d.status,
    d.delay_minutes,
    d.distance_km,
    d.weight_kg
FROM delivery d
JOIN cities c ON d.city = c.city_name
JOIN carriers cr ON d.carrier = cr.carrier_name;
""")

conn.commit()
conn.close()

print("Normalization completed")
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("deliveries.db")

#Queries
queries = {
    "Total Deliveries per Carrier": """
        SELECT cr.carrier_name, COUNT(*) AS total_deliveries
        FROM deliveries d
        JOIN carriers cr ON d.carrier_id = cr.carrier_id
        GROUP BY cr.carrier_name
        ORDER BY total_deliveries DESC;
    """,
    "Average Delivery Distance per Carrier": """
        SELECT cr.carrier_name, ROUND(AVG(d.distance_km),2) AS avg_distance
        FROM deliveries d
        JOIN carriers cr ON d.carrier_id = cr.carrier_id
        GROUP BY cr.carrier_name
        ORDER BY avg_distance DESC;
    """,
    "Deliveries with Delay > 30 Minutes": """
        SELECT d.delivery_id, c.city_name, cr.carrier_name, d.delay_minutes
        FROM deliveries d
        JOIN cities c ON d.city_id = c.city_id
        JOIN carriers cr ON d.carrier_id = cr.carrier_id
        WHERE d.delay_minutes > 30
        ORDER BY d.delay_minutes DESC;
    """,
    "Top 5 Customers by Total Deliveries": """
        SELECT d.customer_id, COUNT(*) AS total_deliveries
        FROM deliveries d
        GROUP BY d.customer_id
        ORDER BY total_deliveries DESC
        LIMIT 5;
    """,
    "Average Weight and Distance per City": """
        SELECT c.city_name, ROUND(AVG(d.weight_kg),2) AS avg_weight,
               ROUND(AVG(d.distance_km),2) AS avg_distance
        FROM deliveries d
        JOIN cities c ON d.city_id = c.city_id
        GROUP BY c.city_name
        ORDER BY avg_distance DESC;
    """
}

# Execute queries and print results
for name, query in queries.items():
    print(f"\n=== {name} ===")
    df = pd.read_sql_query(query, conn)
    print(df)

conn.close()
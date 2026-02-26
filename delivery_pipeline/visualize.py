import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("deliveries.db")

# -------------------------------
# 1 Total Deliveries per Carrier
# -------------------------------
query1 = """
SELECT cr.carrier_name, COUNT(*) AS total_deliveries
FROM deliveries d
JOIN carriers cr ON d.carrier_id = cr.carrier_id
GROUP BY cr.carrier_name
ORDER BY total_deliveries DESC;
"""

df1 = pd.read_sql_query(query1, conn)
print("\n=== Total Deliveries per Carrier ===")
print(df1)

plt.figure()
plt.bar(df1["carrier_name"], df1["total_deliveries"])
plt.title("Total Deliveries per Carrier")
plt.xlabel("Carrier")
plt.ylabel("Total Deliveries")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# -------------------------------
# 2 Average Distance per Carrier
# -------------------------------
query2 = """
SELECT cr.carrier_name, ROUND(AVG(d.distance_km),2) AS avg_distance
FROM deliveries d
JOIN carriers cr ON d.carrier_id = cr.carrier_id
GROUP BY cr.carrier_name
ORDER BY avg_distance DESC;
"""

df2 = pd.read_sql_query(query2, conn)
print("\n=== Average Distance per Carrier ===")
print(df2)

plt.figure()
plt.bar(df2["carrier_name"], df2["avg_distance"])
plt.title("Average Distance per Carrier")
plt.xlabel("Carrier")
plt.ylabel("Average Distance (km)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# -------------------------------
# 3 Average Weight per City
# -------------------------------
query3 = """
SELECT c.city_name, ROUND(AVG(d.weight_kg),2) AS avg_weight
FROM deliveries d
JOIN cities c ON d.city_id = c.city_id
GROUP BY c.city_name
ORDER BY avg_weight DESC;
"""

df3 = pd.read_sql_query(query3, conn)
print("\n=== Average Weight per City ===")
print(df3)

plt.figure()
plt.bar(df3["city_name"], df3["avg_weight"])
plt.title("Average Delivery Weight per City")
plt.xlabel("City")
plt.ylabel("Average Weight (kg)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


conn.close()
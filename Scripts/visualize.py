import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# 1️⃣ Connect to SQL Server
# -------------------------------
server = r'NBDBNPF3W63YL\DEVELOPER19'
database = 'Jabulani'
username = 'sa'
password = 'Mjey@yahoo1'

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    f'SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=no'
)

# -------------------------------
# 2️⃣ Read delivery data into DataFrame
# -------------------------------
query = "SELECT * FROM DeliveryData"
delivery_df = pd.read_sql(query, conn)

# Close the connection
conn.close()

# -------------------------------
# 3️⃣ Visualization Settings
# -------------------------------
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10,6)

# -------------------------------
# 4️⃣ Total deliveries by status
# -------------------------------
status_counts = delivery_df['status'].value_counts()
sns.barplot(x=status_counts.index, y=status_counts.values, palette="viridis")
plt.title("Total Deliveries by Status")
plt.ylabel("Number of Deliveries")
plt.show()

# -------------------------------
# 5️⃣ Average delay by city
# -------------------------------
avg_delay_city = delivery_df.groupby('city')['delay_minutes'].mean().sort_values(ascending=False)
sns.barplot(x=avg_delay_city.index, y=avg_delay_city.values, palette="magma")
plt.title("Average Delay by City")
plt.ylabel("Average Delay (minutes)")
plt.xticks(rotation=45)
plt.show()

# -------------------------------
# 6️⃣ Top carriers by number of deliveries
# -------------------------------
carrier_counts = delivery_df['carrier'].value_counts()
sns.barplot(x=carrier_counts.index, y=carrier_counts.values, palette="coolwarm")
plt.title("Deliveries by Carrier")
plt.ylabel("Number of Deliveries")
plt.show()

# -------------------------------
# 7️⃣ On-time vs Late Deliveries
# -------------------------------
delivery_df['delivery_status'] = delivery_df['delay_minutes'].apply(lambda x: 'On-time' if x==0 else 'Late')
status_counts2 = delivery_df['delivery_status'].value_counts()
sns.barplot(x=status_counts2.index, y=status_counts2.values, palette="Set2")
plt.title("On-time vs Late Deliveries")
plt.ylabel("Number of Deliveries")
plt.show()

# -------------------------------
# 8️⃣ Monthly delivery trends
# -------------------------------
delivery_df['month'] = pd.to_datetime(delivery_df['scheduled_datetime']).dt.to_period('M')
monthly_counts = delivery_df.groupby('month').size()
monthly_counts.plot(kind='line', marker='o')
plt.title("Monthly Delivery Trends")
plt.ylabel("Number of Deliveries")
plt.xticks(rotation=45)
plt.show()

# -------------------------------
# 9️⃣ Scatter: Distance vs Weight
# -------------------------------
sns.scatterplot(data=delivery_df, x='distance_km', y='weight_kg', hue='carrier')
plt.title("Distance vs Weight by Carrier")
plt.show()

# -------------------------------
# 🔟 Correlation Heatmap
# -------------------------------
sns.heatmap(delivery_df[['delay_minutes','distance_km','weight_kg']].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()

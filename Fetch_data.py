from ucimlrepo import fetch_ucirepo
import pandas as pd

# ✅ Step 1: Fetch dataset from UCI (Online Retail Dataset, ID = 352)
online_retail = fetch_ucirepo(id=352)

# ✅ Step 2: Load data as pandas DataFrames
dataframe1 = online_retail.data.features   # Feature columns
dataframe2 = online_retail.data.targets    # Target columns (empty for this dataset)

# ✅ Step 3: Print metadata
print("📘 Dataset Metadata:\n")
print(online_retail.metadata)

# ✅ Step 4: Print variable descriptions
print("\n🧾 Variable Descriptions:\n")
print(online_retail.variables)

# ✅ Step 5: Save to CSV in local 'data lake'
output_path = r"C:\Users\Jabulani.Mcineka\OneDrive - AHRI\Desktop\My Projects\DataLake project\Fetched_data.csv"
dataframe1.to_csv(output_path, index=False)

print("\n✅ Data saved successfully to:")
print(output_path)

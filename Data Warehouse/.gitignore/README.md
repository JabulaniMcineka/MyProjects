# Sales Data Warehouse Project

This project shows how to create a small **Sales Data Warehouse** using SQLite and analyze sales data using Python.

---

## Project Structure

sales_dw_project/
│
├── data/ # CSV files
│ ├── sales.csv
│ ├── products.csv
│ ├── customers.csv
│ └── regions.csv
│
├── scripts/ # Python scripts
│ ├── create_dw.py # Create database and tables
│ └── data_wrangling.py # Load CSVs and clean data
│
├── .gitignore
└── README.md

pgsql
Copy
Edit

---

## What This Project Does

1. **Create the database**  
   Make a SQLite database with **Product, Customer, Region, and Sales** tables.

2. **Load data from CSV files**  
   Put your CSV files in the `data/` folder and load them into the database.

3. **Clean and prepare the data**  
   - Fill missing values  
   - Rename columns  
   - Join tables together  
   - Add new columns (like monthly sales or high-value sales)

4. **Analyze the data (EDA)**  
   - Count rows and unique values  
   - Check averages, totals, min, max  
   - Compare sales by region, product, or customer  
   - Make charts and plots to see trends

---

## How to Run

1. **Create the database**  

```bash
python scripts/create_dw.py
Load and clean the data

bash
Copy
Edit
python scripts/data_wrangling.py
Explore the data

Open the Jupyter notebook:

bash
Copy
Edit
jupyter notebook notebooks/01_eda_sales.ipynb
Tools Used
Python

SQLite

Pandas

Matplotlib / Seaborn

Notes
Put your CSV files in the data/ folder.

The database file sales_dw.db will be created in the data/ folder.

Install required Python packages:

bash
Copy
Edit
pip install pandas matplotlib seaborn
pgsql
Copy
Edit

---

Copy **everything inside the triple backticks above** and paste it into your GitHub `README.md`.  

Once you save/commit it, your repository will show this README on the main page.  

If you want, I can also make a **more colorful beginner version with emojis and section highlights** so it’

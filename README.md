# My Data Projects

This repository contains two beginner-friendly data projects demonstrating **data analysis, cleaning, and visualization** using Python and SQLite.

---

## 1️⃣ Sales Data Warehouse Project

Create a small **Sales Data Warehouse** and analyze sales data.

### Project Structure

sales_dw_project/
├── data/ # CSV files
│ ├── sales.csv
│ ├── products.csv
│ ├── customers.csv
│ └── regions.csv
├── scripts/ # Python scripts
│ ├── create_dw.py
│ └── data_wrangling.py
└── notebooks/
└── 01_eda_sales.ipynb


### How to Run
python scripts/create_dw.py
python scripts/data_wrangling.py
jupyter notebook notebooks/01_eda_sales.ipynb


2️⃣ Facility Visits Analysis Project
Analyze patient visit and demographic data.

Project Structure

facility_visits_analysis/
├── data/
│   ├── Persons.csv
│   └── FacilityVisits.csv
├── scripts/
│   ├── facility_visits_analysis.py
│   └── Scrap.py
└── output/                # Cleaned data & plots (created after running the script)


How to Run
mkdir output
python scripts/facility_visits_analysis.py

Tools Used
Python

SQLite

Pandas

Matplotlib / Seaborn


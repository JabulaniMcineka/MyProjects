# 🚚 Delivery Pipeline Project

A data engineering pipeline that generates synthetic delivery data, loads it into a normalised SQLite database, and prepares it for downstream analysis. This project is the foundation for the [Delivery Analysis Project](../delivery_analysis/).

---

## 🏗️ Architecture

```
Python Data Generator
        │
        ▼
delivery_data.csv (250 records)
        │
        ▼
ETL / Data Transformation
        │
        ▼
SQLite Database (Delivery.db)
   ├── deliveries
   ├── customers
   ├── carriers
   └── cities
        │
        ▼
SQL Queries & Validation
        │
        ▼
Ready for Analysis & Dashboards
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Data generation & ETL scripting |
| SQLite | Normalised relational database |
| SQL | Schema creation, inserts & queries |
| Pandas | Data transformation & CSV export |

---

## 📁 Project Structure

```
delivery_pipeline/
├── schema.sql           # Database schema — table definitions
├── insert_data.sql      # SQL inserts — populates all tables
├── delivery_data.csv    # Generated synthetic dataset (250 records)
├── pipeline.py          # Python ETL script (generate → transform → load)
└── README.md
```

---

## 🗃️ Database Schema

### Tables

**`deliveries`** — Core delivery records
- `delivery_id` (PK), `customer_id` (FK), `carrier_id` (FK), `city_id` (FK)
- `scheduled_datetime`, `delivered_datetime`, `status`, `delay_minutes`
- `distance_km`, `weight_kg`

**`customers`** — Customer master data
- `customer_id` (PK), `customer_name`

**`carriers`** — Carrier master data
- `carrier_id` (PK), `carrier_name`
- Carriers: SwiftX, MegaHaul, SkyDrop

**`cities`** — City reference table
- `city_id` (PK), `city_name`
- Cities: Johannesburg, Cape Town, Durban, Pretoria, Bloemfontein, Gqeberha

---

## 📊 Dataset

- **250 records** of synthetic delivery data
- **Date range:** January 2025 – June 2025
- **Status values:** Delivered / Pending / Failed
- **Generated via Python** to simulate real-world logistics data

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install pandas
```

### Option 1 — Run the Python pipeline

```bash
python pipeline.py
```

This will generate the dataset, transform it, and load it into `Delivery.db` automatically.

### Option 2 — Run SQL manually

1. Open SQLite:
```bash
sqlite3 Delivery.db
```

2. Create the schema:
```bash
.read schema.sql
```

3. Insert the data:
```bash
.read insert_data.sql
```

---

## 🔄 Pipeline Stages

| Stage | Description |
|-------|-------------|
| **Generate** | Python script creates 250 synthetic delivery records |
| **Transform** | Data cleaned, typed, and split into normalised tables |
| **Load** | Records inserted into SQLite via `insert_data.sql` or Python |
| **Validate** | Row counts and null checks confirm data integrity |
| **Export** | `delivery_data.csv` exported for use in analysis notebook |

---

## 🔗 Downstream Project

This pipeline feeds directly into the **Delivery Analysis Project**, which runs 12 SQL queries, 9 data quality checks, and generates a 6-chart visualisation dashboard.

👉 [View Delivery Analysis](../delivery_analysis/)  
👉 [Open Analysis in Colab](https://colab.research.google.com/drive/1z2i-ZGICFlbVb-wdma4U47S0bYlJ3cGC?usp=sharing)

---

## 👤 Author

**Jabulani Mcineka**

- 🏅 AWS Certified Cloud Practitioner (2025)
- 🏅 AWS Certified Data Engineer – Associate (2025)
- 🎓 Postgraduate Diploma in Computer Science — Tshwane University of Technology
- [LinkedIn](https://www.linkedin.com/in/jabulani-mcineka)
- [GitHub](https://github.com/JabulaniMcineka)

---

## 📄 License

MIT

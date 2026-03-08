#  E-Commerce Real-Time Data Pipeline

> A production-grade data engineering pipeline built on AWS Free Tier — ingesting, transforming, and serving e-commerce data using Python, S3, Glue, Athena, and Airflow.

---

##  Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Fake Store API │────▶│  AWS S3 Raw  │────▶│  AWS S3 Silver   │────▶│ AWS Athena  │
│  (Source)       │     │  (JSON)      │     │  (Parquet)       │     │ (SQL Query) │
└─────────────────┘     └──────────────┘     └──────────────────┘     └─────────────┘
        │                      │                      │
        │               AWS Glue Crawler        AWS Glue ETL
        │                                             │
        └──────────── Apache Airflow DAG (Orchestration) ──────────────┘

└──────────────────┘
---

##  Screenshots

###  Airflow DAG — All 4 Tasks Green
![Airflow DAG](https://raw.githubusercontent.com/JabulaniMcineka/MyProjects/main/ecommerce-data-pipeline/screenshots/airflow_dag.png)

###  AWS S3 Buckets — Raw & Silver
![S3 Buckets](https://raw.githubusercontent.com/JabulaniMcineka/MyProjects/main/ecommerce-data-pipeline/screenshots/s3_buckets.png)


###  Athena Query Results — Silver Tables
![Athena Results](https://raw.githubusercontent.com/JabulaniMcineka/MyProjects/main/ecommerce-data-pipeline/screenshots/athena_results.png)

---

### Medallion Architecture
| Layer | Location | Format | Description |
|---|---|---|---|
| **Raw** | `s3://ecommerce-data-pipeline-raw/raw/` | JSON | Unmodified API data |
| **Silver** | `s3://ecommerce-data-pipeline-silver/silver/` | Parquet | Cleaned & typed |
| **Gold** | Athena Views | SQL Views | Aggregated for reporting |

---

##  Tech Stack

| Tool | Purpose | Cost |
|---|---|---|
| Python 3.11 | Ingestion & transformation | Free |
| AWS S3 | Data lake storage | Free tier |
| AWS Glue | Crawling & cataloging | Free tier |
| AWS Athena | SQL querying | Free tier |
| Apache Airflow | Orchestration | Free (Docker) |
| Docker Compose | Local environment | Free |
| GitHub Actions | CI/CD | Free |

---

##  Project Structure

```
ecommerce-data-pipeline/
├── ingestion/
│   └── ingest.py           # API → S3 Raw
├── transformation/
│   └── transform.py        # Raw JSON → Silver Parquet
├── orchestration/
│   └── dags/
│       └── ecommerce_dag.py # Airflow DAG
├── infrastructure/
│   └── setup_aws.py        # One-time AWS setup
├── tests/
│   └── validate.py         # Data quality checks
├── docker-compose.yml      # Local Airflow stack
├── requirements.txt
└── README.md
```

---

##  Getting Started

### Prerequisites
- Python 3.11+
- Docker Desktop
- AWS CLI configured (`aws configure`)
- AWS account (Free Tier)

### 1. Clone the repo
```bash
git clone https://github.com/JabulaniMcineka/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up AWS infrastructure (run once)
```bash
python infrastructure/setup_aws.py
```

### 4. Start Airflow locally
```bash
docker-compose up -d
```
Visit **http://localhost:8080** — login: `admin` / `admin`

### 5. Trigger the pipeline manually
```bash
# Or trigger via Airflow UI
python ingestion/ingest.py
python transformation/transform.py
python tests/validate.py
```

---

##  Data Model

### Products (Silver)
| Column | Type | Description |
|---|---|---|
| id | INT | Product ID |
| title | STRING | Product name |
| price | FLOAT | Price in USD |
| category | STRING | Product category |
| rating_rate | FLOAT | Average rating |
| rating_count | INT | Number of ratings |
| ingested_at | TIMESTAMP | Pipeline run time |

### Users (Silver)
| Column | Type | Description |
|---|---|---|
| id | INT | User ID |
| username | STRING | Username |
| email | STRING | Email address |
| first_name | STRING | First name |
| last_name | STRING | Last name |
| city | STRING | City |
| ingested_at | TIMESTAMP | Pipeline run time |

### Carts (Silver)
| Column | Type | Description |
|---|---|---|
| id | INT | Cart ID |
| userId | INT | User ID (FK) |
| date | DATE | Cart date |
| product_id | INT | Product ID (FK) |
| quantity | INT | Quantity ordered |
| ingested_at | TIMESTAMP | Pipeline run time |

---

##  Example Athena Queries

```sql
-- Top selling product categories
SELECT category, COUNT(*) as orders, SUM(quantity) as total_units
FROM ecommerce_silver.carts c
JOIN ecommerce_silver.products p ON c.product_id = p.id
GROUP BY category
ORDER BY total_units DESC;

-- Revenue by category
SELECT p.category, ROUND(SUM(p.price * c.quantity), 2) as revenue
FROM ecommerce_silver.carts c
JOIN ecommerce_silver.products p ON c.product_id = p.id
GROUP BY p.category
ORDER BY revenue DESC;

-- Most active users
SELECT u.username, u.city, COUNT(*) as cart_items
FROM ecommerce_silver.carts c
JOIN ecommerce_silver.users u ON c.userId = u.id
GROUP BY u.username, u.city
ORDER BY cart_items DESC
LIMIT 10;
```

---

##  Data Quality Checks

The pipeline runs automated checks after each load:
-  Row count > 0 for all tables
-  No null or zero prices in products
-  No invalid quantities in carts
-  Schema validation on each run

---

##  Pipeline Schedule

The Airflow DAG runs daily at **6:00 AM UTC**:
1. `ingest_raw_data` — Pulls from Fake Store API → S3 Raw
2. `transform_to_silver` — Cleans & writes Parquet → S3 Silver
3. `run_glue_crawler` — Updates Athena catalog
4. `validate_data_quality` — Runs quality checks

---

##  Author

**Jabulani Mcineka**
- AWS Certified Cloud Practitioner
- Data Engineering Certified
- Postgraduate Diploma in Computer Science

---

##  License
MIT

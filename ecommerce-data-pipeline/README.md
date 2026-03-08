# 🛒 E-Commerce Real-Time Data Pipeline

> A production-grade data engineering pipeline built on AWS Free Tier — ingesting, transforming, and serving e-commerce data using Python, S3, Glue, Athena, and Apache Airflow.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![AWS](https://img.shields.io/badge/AWS-Free%20Tier-orange)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.8.1-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Status](https://img.shields.io/badge/Pipeline-✅%20Running-brightgreen)

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Fake Store API │────▶│  AWS S3 Raw  │────▶│  AWS S3 Silver   │────▶│ AWS Athena  │
│  (Source)       │     │  (JSON)      │     │  (Parquet)       │     │ (SQL Query) │
└─────────────────┘     └──────────────┘     └──────────────────┘     └─────────────┘
        │                      │                      │
        │               AWS Glue Crawler        AWS Glue ETL
        │                                             │
        └──────────── Apache Airflow DAG (Orchestration) ──────────────┘
```

### Medallion Architecture
| Layer | Location | Format | Description |
|---|---|---|---|
| **Raw** | `s3://ecommerce-pipeline-raw-{account_id}/raw/` | JSON | Unmodified API data |
| **Silver** | `s3://ecommerce-pipeline-silver-{account_id}/silver/` | Parquet | Cleaned & typed |
| **Gold** | Athena Views | SQL Views | Aggregated for reporting |

---

## 📸 Screenshots

### ✅ Airflow DAG — All 4 Tasks Green
![Airflow DAG](https://raw.githubusercontent.com/JabulaniMcineka/MyProjects/main/ecommerce-data-pipeline/screenshots/airflow_dag.png)

### 🪣 AWS S3 Buckets — Raw & Silver
![S3 Buckets](https://raw.githubusercontent.com/JabulaniMcineka/MyProjects/main/ecommerce-data-pipeline/screenshots/s3_buckets.png)

### 🔍 Athena Query Results — Silver Tables
![Athena Results](https://raw.githubusercontent.com/JabulaniMcineka/MyProjects/main/ecommerce-data-pipeline/screenshots/athena_results.png)

---

## 🛠️ Tech Stack

| Tool | Version | Purpose | Cost |
|---|---|---|---|
| Python | 3.12 | Ingestion & transformation scripts | Free |
| AWS S3 | Free Tier | Data lake storage (Raw & Silver zones) | Free |
| AWS Glue | Free Tier | Crawling & Athena table cataloging | Free |
| AWS Athena | Free Tier | SQL querying on Parquet files | Free |
| Apache Airflow | 2.8.1 | Pipeline orchestration & scheduling | Free (Docker) |
| Docker Compose | Latest | Local Airflow environment | Free |
| PostgreSQL | 13 | Airflow metadata database | Free |

---

## 📁 Project Structure

```
ecommerce-data-pipeline/
├── ingestion/
│   └── ingest.py               # Fake Store API → S3 Raw (JSON)
├── transformation/
│   └── transform.py            # Raw JSON → Silver Parquet
├── orchestration/
│   └── dags/
│       └── ecommerce_dag.py    # Airflow DAG (daily @ 6AM UTC)
├── infrastructure/
│   └── setup_aws.py            # One-time AWS bootstrap
├── tests/
│   └── validate.py             # Data quality checks via Athena
├── docker-compose.yml          # Local Airflow stack
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

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

### 3. Configure AWS credentials
```bash
aws configure
```
Enter your Access Key ID, Secret Access Key, region (`us-east-1`), and output format (`json`).

### 4. Set up AWS infrastructure (run once)
```bash
python infrastructure/setup_aws.py
```
This creates S3 buckets, IAM role, Glue crawler, and Athena database.

> ⚠️ **Note:** S3 bucket names must be globally unique. Update `RAW_BUCKET` and `SILVER_BUCKET` in `setup_aws.py`, `ingest.py`, and `transform.py` to include your AWS account ID as a suffix.

### 5. Start Airflow locally
```bash
docker-compose up -d
```
Visit **http://localhost:8080** — login: `admin` / `admin`

### 6. Trigger the pipeline
- Enable the `ecommerce_pipeline` DAG in the Airflow UI
- Click **▶ Trigger DAG** to run manually
- Or run scripts directly:

```bash
python ingestion/ingest.py
python transformation/transform.py
python tests/validate.py
```

---

## 🔄 Airflow DAG

The DAG runs daily at **6:00 AM UTC**:

```
ingest_raw_data → transform_to_silver → run_glue_crawler → validate_data_quality
```

| Task | Operator | Description |
|---|---|---|
| `ingest_raw_data` | BashOperator | Pulls from Fake Store API → S3 Raw |
| `transform_to_silver` | BashOperator | Cleans & writes Parquet → S3 Silver |
| `run_glue_crawler` | BashOperator | Updates Athena catalog |
| `validate_data_quality` | BashOperator | Runs data quality checks |

---

## 📊 Data Model

### Products (Silver)
| Column | Type | Description |
|---|---|---|
| id | INT | Product ID |
| title | STRING | Product name |
| price | FLOAT | Price in USD |
| category | STRING | Product category (normalised) |
| rating_rate | FLOAT | Average customer rating |
| rating_count | INT | Number of ratings |
| ingested_at | TIMESTAMP | Pipeline run timestamp |

### Users (Silver)
| Column | Type | Description |
|---|---|---|
| id | INT | User ID |
| username | STRING | Username |
| email | STRING | Email address |
| first_name | STRING | First name |
| last_name | STRING | Last name |
| city | STRING | City |
| ingested_at | TIMESTAMP | Pipeline run timestamp |

### Carts (Silver)
| Column | Type | Description |
|---|---|---|
| id | INT | Cart ID |
| userId | INT | User ID (FK → users.id) |
| date | DATE | Cart creation date |
| product_id | INT | Product ID (FK → products.id) |
| quantity | INT | Quantity ordered |
| ingested_at | TIMESTAMP | Pipeline run timestamp |

---

## 🔍 Example Athena Queries

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

## ✅ Data Quality Checks

Automated checks run after every load via AWS Athena:

| Check | Query | Expected |
|---|---|---|
| `products_row_count` | COUNT(*) on products | > 0 |
| `products_no_null_price` | WHERE price IS NULL OR price <= 0 | = 0 |
| `users_row_count` | COUNT(*) on users | > 0 |
| `carts_valid_quantities` | WHERE quantity <= 0 | = 0 |

---

## 🐛 Troubleshooting

| Issue | Fix |
|---|---|
| `InvalidAccessKeyId` | Run `aws configure` with fresh keys from AWS Console |
| `BucketAlreadyExists` | S3 names are global — add your AWS account ID as suffix |
| `AccessDenied` on S3 | Attach `AmazonS3FullAccess` policy to your IAM user |
| Airflow DAG not showing | Ensure `ecommerce_dag.py` is in `orchestration/dags/` |
| Athena table not found | Run Glue crawler before validation |
| Docker webserver not starting | Ensure `airflow-init` completes before webserver starts |

---

## 👤 Author

**Jabulani Mcineka**
- 🏅 AWS Certified Cloud Practitioner (2025)
- 🏅 AWS Certified Data Engineer – Associate (2025)
- 🎓 Postgraduate Diploma in Computer Science — Tshwane University of Technology
- 🔗 [LinkedIn](https://www.linkedin.com/in/jabulani-mcineka-941360182)
- 💻 [GitHub](https://github.com/JabulaniMcineka)

---

## 📄 License
MIT

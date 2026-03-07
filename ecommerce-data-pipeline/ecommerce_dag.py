"""
Airflow DAG — Orchestrates the full e-commerce data pipeline
Schedule: Daily at 6AM UTC
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "jabulani",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ecommerce_pipeline",
    default_args=default_args,
    description="E-Commerce ETL: API → S3 Raw → S3 Silver → Athena",
    schedule_interval="0 6 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ecommerce", "etl", "s3", "aws"],
) as dag:

    # Step 1: Ingest raw data from API to S3
    ingest = BashOperator(
        task_id="ingest_raw_data",
        bash_command="cd /opt/airflow/project && python ingestion/ingest.py",
    )

    # Step 2: Transform raw → silver
    transform = BashOperator(
        task_id="transform_to_silver",
        bash_command="cd /opt/airflow/project && python transformation/transform.py",
    )

    # Step 3: Run Glue crawler to update Athena catalog
    crawl = BashOperator(
        task_id="run_glue_crawler",
        bash_command="""
            aws glue start-crawler --name ecommerce-silver-crawler
            echo "Crawler started"
        """,
    )

    # Step 4: Validate row counts via Athena
    validate = BashOperator(
        task_id="validate_data_quality",
        bash_command="cd /opt/airflow/project && python tests/validate.py",
    )

    # DAG flow
    ingest >> transform >> crawl >> validate

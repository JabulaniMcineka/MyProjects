"""
Data Quality Validation — Queries Athena silver tables and checks row counts,
nulls, and basic business rules. Raises on failure.
"""

import boto3
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ATHENA_DB      = "ecommerce_silver"
ATHENA_OUTPUT  = "s3://ecommerce-data-pipeline-silver/athena-results/"
athena         = boto3.client("athena", region_name="us-east-1")

QUALITY_CHECKS = [
    {
        "name": "products_row_count",
        "query": "SELECT COUNT(*) as cnt FROM ecommerce_silver.products",
        "check": lambda r: int(r) > 0,
        "message": "Products table is empty!",
    },
    {
        "name": "products_no_null_price",
        "query": "SELECT COUNT(*) FROM ecommerce_silver.products WHERE price IS NULL OR price <= 0",
        "check": lambda r: int(r) == 0,
        "message": "Products table has null/zero prices!",
    },
    {
        "name": "users_row_count",
        "query": "SELECT COUNT(*) FROM ecommerce_silver.users",
        "check": lambda r: int(r) > 0,
        "message": "Users table is empty!",
    },
    {
        "name": "carts_valid_quantities",
        "query": "SELECT COUNT(*) FROM ecommerce_silver.carts WHERE quantity <= 0",
        "check": lambda r: int(r) == 0,
        "message": "Carts table has invalid quantities!",
    },
]


def run_query(sql: str) -> str:
    response = athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={"Database": ATHENA_DB},
        ResultConfiguration={"OutputLocation": ATHENA_OUTPUT},
    )
    execution_id = response["QueryExecutionId"]

    # Wait for completion
    while True:
        result = athena.get_query_execution(QueryExecutionId=execution_id)
        state  = result["QueryExecution"]["Status"]["State"]
        if state in ("SUCCEEDED", "FAILED", "CANCELLED"):
            break
        time.sleep(2)

    if state != "SUCCEEDED":
        raise Exception(f"Query failed: {sql}")

    rows = athena.get_query_results(QueryExecutionId=execution_id)
    return rows["ResultSet"]["Rows"][1]["Data"][0]["VarCharValue"]


def run():
    failures = []
    for check in QUALITY_CHECKS:
        logger.info(f"Running check: {check['name']}")
        result = run_query(check["query"])
        passed = check["check"](result)
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status} — {check['name']} (result={result})")
        if not passed:
            failures.append(check["message"])

    if failures:
        raise ValueError(f"Data quality failures:\n" + "\n".join(failures))
    logger.info("All data quality checks passed!")


if __name__ == "__main__":
    run()

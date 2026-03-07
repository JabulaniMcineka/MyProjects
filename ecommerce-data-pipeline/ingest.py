"""
Ingestion Layer — Fake Store API → AWS S3 (Raw Zone)
Pulls products, orders, and users from public API and lands as JSON in S3.
"""

import json
import boto3
import requests
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
S3_BUCKET = "ecommerce-data-pipeline-raw"
API_BASE  = "https://fakestoreapi.com"
ENDPOINTS = {
    "products": "/products",
    "users":    "/users",
    "carts":    "/carts",
}

s3 = boto3.client("s3")


def fetch(endpoint: str) -> list:
    url = f"{API_BASE}{endpoint}"
    logger.info(f"Fetching {url}")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def upload_to_s3(data: list, entity: str) -> str:
    today = datetime.utcnow().strftime("%Y/%m/%d")
    timestamp = datetime.utcnow().strftime("%H%M%S")
    key = f"raw/{entity}/{today}/{entity}_{timestamp}.json"

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(data, indent=2),
        ContentType="application/json",
    )
    logger.info(f"Uploaded s3://{S3_BUCKET}/{key}")
    return key


def run():
    results = {}
    for entity, endpoint in ENDPOINTS.items():
        data = fetch(endpoint)
        key  = upload_to_s3(data, entity)
        results[entity] = {"records": len(data), "s3_key": key}
        logger.info(f"{entity}: {len(data)} records ingested")
    return results


if __name__ == "__main__":
    run()

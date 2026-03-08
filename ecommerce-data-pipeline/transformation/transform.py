"""
Transformation Layer — Raw JSON → Silver (cleaned Parquet) via AWS Glue / local PySpark
Reads raw JSON from S3, cleans and enriches, writes Parquet to silver zone.
"""

import boto3
import json
import pandas as pd
from io import StringIO
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

S3_BUCKET = "ecommerce-pipeline-raw-797795454172"
S3_SILVER = "ecommerce-pipeline-silver-797795454172"


def read_latest_raw(entity: str) -> pd.DataFrame:
    s3 = boto3.client("s3")
    today = datetime.utcnow().strftime("%Y/%m/%d")
    prefix = f"raw/{entity}/{today}/"

    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)
    if "Contents" not in response:
        raise FileNotFoundError(f"No raw files found for {entity} on {today}")

    # Get latest file
    latest = sorted(response["Contents"], key=lambda x: x["LastModified"])[-1]
    obj = s3.get_object(Bucket=S3_BUCKET, Key=latest["Key"])
    data = json.loads(obj["Body"].read())
    logger.info(f"Read {len(data)} records from {latest['Key']}")
    return pd.DataFrame(data)


def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ingested_at"] = datetime.utcnow().isoformat()
    df["price"] = df["price"].astype(float).round(2)
    df["category"] = df["category"].str.strip().str.lower()

    # Flatten rating column
    df["rating_rate"]  = df["rating"].apply(lambda x: x.get("rate", 0) if isinstance(x, dict) else 0)
    df["rating_count"] = df["rating"].apply(lambda x: x.get("count", 0) if isinstance(x, dict) else 0)
    df.drop(columns=["rating"], inplace=True)

    return df[["id", "title", "price", "category", "rating_rate", "rating_count", "ingested_at"]]


def transform_users(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ingested_at"] = datetime.utcnow().isoformat()

    # Flatten address
    df["city"]    = df["address"].apply(lambda x: x.get("city", "") if isinstance(x, dict) else "")
    df["zipcode"] = df["address"].apply(lambda x: x.get("zipcode", "") if isinstance(x, dict) else "")
    df["lat"]     = df["address"].apply(lambda x: x.get("geolocation", {}).get("lat", "") if isinstance(x, dict) else "")
    df["long"]    = df["address"].apply(lambda x: x.get("geolocation", {}).get("long", "") if isinstance(x, dict) else "")

    # Flatten name
    df["first_name"] = df["name"].apply(lambda x: x.get("firstname", "") if isinstance(x, dict) else "")
    df["last_name"]  = df["name"].apply(lambda x: x.get("lastname", "") if isinstance(x, dict) else "")

    df.drop(columns=["address", "name"], inplace=True)
    return df[["id", "username", "email", "first_name", "last_name", "city", "zipcode", "ingested_at"]]


def transform_carts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ingested_at"] = datetime.utcnow().isoformat()
    df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)

    # Explode products in cart
    df = df.explode("products").reset_index(drop=True)
    df["product_id"] = df["products"].apply(lambda x: x.get("productId") if isinstance(x, dict) else None)
    df["quantity"]   = df["products"].apply(lambda x: x.get("quantity") if isinstance(x, dict) else None)
    df.drop(columns=["products"], inplace=True)

    return df[["id", "userId", "date", "product_id", "quantity", "ingested_at"]]


TRANSFORMERS = {
    "products": transform_products,
    "users":    transform_users,
    "carts":    transform_carts,
}


def write_silver(df: pd.DataFrame, entity: str):
    s3 = boto3.client("s3")
    today = datetime.utcnow().strftime("%Y/%m/%d")
    key = f"silver/{entity}/{today}/{entity}.parquet"

    buffer = df.to_parquet(index=False)
    s3.put_object(Bucket=S3_SILVER, Key=key, Body=buffer)
    logger.info(f"Written silver: s3://{S3_SILVER}/{key} ({len(df)} rows)")


def run():
    for entity, transformer in TRANSFORMERS.items():
        logger.info(f"Transforming {entity}...")
        raw_df    = read_latest_raw(entity)
        silver_df = transformer(raw_df)
        write_silver(silver_df, entity)
        logger.info(f"{entity} done: {len(silver_df)} rows")


if __name__ == "__main__":
    run()

"""
Infrastructure Setup — Creates all AWS resources needed for the pipeline.
Run once to bootstrap your environment. Uses only AWS Free Tier resources.
"""

import boto3
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REGION          = "us-east-1"
RAW_BUCKET      = "ecommerce-data-pipeline-raw"
SILVER_BUCKET   = "ecommerce-data-pipeline-silver"
GLUE_ROLE_NAME  = "ecommerce-glue-role"
CRAWLER_NAME    = "ecommerce-silver-crawler"
ATHENA_DB       = "ecommerce_silver"

s3  = boto3.client("s3",  region_name=REGION)
iam = boto3.client("iam", region_name=REGION)
glue = boto3.client("glue", region_name=REGION)
athena = boto3.client("athena", region_name=REGION)


def create_s3_buckets():
    for bucket in [RAW_BUCKET, SILVER_BUCKET]:
        try:
            s3.create_bucket(Bucket=bucket)
            logger.info(f"Created bucket: {bucket}")
        except s3.exceptions.BucketAlreadyOwnedByYou:
            logger.info(f"Bucket already exists: {bucket}")


def create_glue_role():
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "glue.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    try:
        iam.create_role(
            RoleName=GLUE_ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="Role for Glue crawler and ETL jobs",
        )
        iam.attach_role_policy(
            RoleName=GLUE_ROLE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole",
        )
        iam.attach_role_policy(
            RoleName=GLUE_ROLE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess",
        )
        logger.info(f"Created IAM role: {GLUE_ROLE_NAME}")
    except iam.exceptions.EntityAlreadyExistsException:
        logger.info(f"IAM role already exists: {GLUE_ROLE_NAME}")


def get_role_arn() -> str:
    return iam.get_role(RoleName=GLUE_ROLE_NAME)["Role"]["Arn"]


def create_glue_crawler():
    role_arn = get_role_arn()
    try:
        glue.create_crawler(
            Name=CRAWLER_NAME,
            Role=role_arn,
            DatabaseName=ATHENA_DB,
            Targets={"S3Targets": [{"Path": f"s3://{SILVER_BUCKET}/silver/"}]},
            Schedule="cron(30 6 * * ? *)",  # 6:30 AM UTC daily
            SchemaChangePolicy={
                "UpdateBehavior": "UPDATE_IN_DATABASE",
                "DeleteBehavior": "LOG",
            },
        )
        logger.info(f"Created Glue crawler: {CRAWLER_NAME}")
    except glue.exceptions.AlreadyExistsException:
        logger.info(f"Crawler already exists: {CRAWLER_NAME}")


def create_athena_database():
    athena.start_query_execution(
        QueryString=f"CREATE DATABASE IF NOT EXISTS {ATHENA_DB}",
        ResultConfiguration={"OutputLocation": f"s3://{SILVER_BUCKET}/athena-results/"},
    )
    logger.info(f"Created Athena database: {ATHENA_DB}")


def run():
    logger.info("Setting up AWS infrastructure...")
    create_s3_buckets()
    create_glue_role()
    create_glue_crawler()
    create_athena_database()
    logger.info("✅ Infrastructure setup complete!")
    logger.info(f"  Raw bucket:    s3://{RAW_BUCKET}")
    logger.info(f"  Silver bucket: s3://{SILVER_BUCKET}")
    logger.info(f"  Glue crawler:  {CRAWLER_NAME}")
    logger.info(f"  Athena DB:     {ATHENA_DB}")


if __name__ == "__main__":
    run()

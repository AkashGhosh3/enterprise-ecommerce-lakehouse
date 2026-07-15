from botocore.exceptions import ClientError

from config.logger import logger
from config.settings import settings
from utils.s3_client import s3_client


def create_bucket(bucket_name: str):
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": settings.AWS_REGION
            }
        )

        logger.success(f"Bucket '{bucket_name}' created successfully.")

    except ClientError as e:
        logger.error(e)


if __name__ == "__main__":
    create_bucket(settings.DATA_LAKE_BUCKET)
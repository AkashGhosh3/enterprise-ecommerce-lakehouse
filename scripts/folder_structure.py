from config.logger import logger
from config.settings import settings
from utils.s3_client import s3_client

FOLDERS = [
    "bronze/customers/",
    "bronze/orders/",
    "bronze/products/",
    "bronze/inventory/",

    "silver/customers/",
    "silver/orders/",
    "silver/products/",
    "silver/inventory/",

    "gold/sales/",
    "gold/customer_analytics/",
    "gold/inventory/"
]


def create_prefix(prefix: str):
    s3_client.put_object(
        Bucket=settings.DATA_LAKE_BUCKET,
        Key=prefix
    )

    logger.info(f"Created {prefix}")


if __name__ == "__main__":
    for folder in FOLDERS:
        create_prefix(folder)

    logger.success("Data Lake folder structure created successfully.")
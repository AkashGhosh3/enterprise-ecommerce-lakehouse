import io
import pandas as pd

from config.settings import settings
from config.logger import logger
from transformations.gold_transform import GoldTransformer
from utils.s3_client import s3_client


BUCKET = settings.DATA_LAKE_BUCKET


def read_all_parquet(prefix):
    """
    Read every parquet file under an S3 prefix.
    """

    paginator = s3_client.get_paginator("list_objects_v2")

    dataframes = []

    for page in paginator.paginate(
        Bucket=BUCKET,
        Prefix=prefix
    ):

        if "Contents" not in page:
            continue

        for obj in page["Contents"]:

            key = obj["Key"]

            if not key.endswith(".parquet"):
                continue

            logger.info(f"Reading {key}")

            response = s3_client.get_object(
                Bucket=BUCKET,
                Key=key
            )

            df = pd.read_parquet(
                io.BytesIO(response["Body"].read())
            )

            dataframes.append(df)

    if not dataframes:
        raise Exception(f"No parquet files found in {prefix}")

    return pd.concat(dataframes, ignore_index=True)


def upload_dataframe(df, key):

    buffer = io.BytesIO()

    df.to_parquet(
        buffer,
        index=False
    )

    buffer.seek(0)

    s3_client.upload_fileobj(
        buffer,
        BUCKET,
        key
    )

    logger.info(f"Uploaded {key}")


def main():

    logger.info("Reading Silver layer...")

    products = read_all_parquet("silver/products/")

    logger.info("Creating Gold summary...")

    summary = GoldTransformer.product_summary(products)

    upload_dataframe(
        summary,
        "gold/products/product_summary.parquet"
    )

    logger.info("Gold layer created successfully.")


if __name__ == "__main__":
    main()
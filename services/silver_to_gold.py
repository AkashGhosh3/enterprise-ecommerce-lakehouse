from datetime import datetime
from io import BytesIO

import pandas as pd

from config.logger import logger
from config.settings import settings
from utils.s3_client import s3_client


class SilverToGoldService:

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name

    def create_product_summary(self, df):

        logger.info("Creating Gold summary...")

        summary = (
            df.groupby("category")
            .agg(
                total_products=("id", "count"),
                average_price=("price", "mean"),
                min_price=("price", "min"),
                max_price=("price", "max")
            )
            .reset_index()
        )

        summary["average_price"] = summary[
            "average_price"
        ].round(2)

        summary["min_price"] = summary[
            "min_price"
        ].round(2)

        summary["max_price"] = summary[
            "max_price"
        ].round(2)

        logger.info(
            f"Created Gold summary with {len(summary)} categories."
        )

        return summary

    def save_to_gold(self, df):

        logger.info("Writing Gold Parquet...")

        now = datetime.utcnow()

        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        timestamp = now.strftime("%Y%m%d_%H%M%S")

        key = (
            f"gold/{self.dataset_name}/"
            f"year={year}/"
            f"month={month}/"
            f"day={day}/"
            f"{timestamp}.parquet"
        )

        buffer = BytesIO()

        df.to_parquet(
            buffer,
            engine="pyarrow",
            index=False
        )

        buffer.seek(0)

        s3_client.put_object(
            Bucket=settings.DATA_LAKE_BUCKET,
            Key=key,
            Body=buffer.getvalue()
        )

        logger.success(f"Uploaded {key}")

        return key
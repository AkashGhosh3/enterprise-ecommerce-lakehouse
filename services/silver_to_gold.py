from datetime import datetime, UTC
from io import BytesIO

import pandas as pd

from config.logger import logger
from config.settings import settings
from utils.metadata_manager import MetadataManager
from utils.s3_client import s3_client


class SilverToGoldService:

    def __init__(self, dataset_name: str = "products"):
        self.dataset_name = dataset_name
        self.metadata = MetadataManager()

    def read_latest_silver(self) -> pd.DataFrame:
        """
        Read the latest Silver dataset from S3.
        """

        key = self.metadata.get_last_file(
            f"{self.dataset_name}_silver"
        )

        logger.info(f"Reading Silver dataset: {key}")

        response = s3_client.get_object(
            Bucket=settings.DATA_LAKE_BUCKET,
            Key=key,
        )

        df = pd.read_parquet(
            BytesIO(response["Body"].read())
        )

        logger.info(
            f"Loaded {len(df)} rows from Silver layer."
        )

        return df

    def create_product_summary(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Create Gold business summary.
        """

        logger.info("Creating Gold summary...")

        summary = (
            df.groupby("category")
            .agg(
                total_products=("id", "count"),
                average_price=("price", "mean"),
                min_price=("price", "min"),
                max_price=("price", "max"),
                average_rating=("rating", "mean"),
                total_reviews=("review_count", "sum"),
            )
            .reset_index()
        )

        summary["average_price"] = (
            summary["average_price"].round(2)
        )

        summary["min_price"] = (
            summary["min_price"].round(2)
        )

        summary["max_price"] = (
            summary["max_price"].round(2)
        )

        summary["average_rating"] = (
            summary["average_rating"].round(2)
        )

        logger.success(
            f"Created Gold summary with {len(summary)} categories."
        )

        return summary

    def save_to_gold(
        self,
        df: pd.DataFrame,
    ) -> str:
        """
        Save Gold dataset to S3.
        """

        logger.info("Writing Gold Parquet...")

        now = datetime.now(UTC)

        key = (
            f"gold/{self.dataset_name}/"
            f"year={now.year}/"
            f"month={now.month:02d}/"
            f"day={now.day:02d}/"
            f"{self.dataset_name}.parquet"
        )

        buffer = BytesIO()

        df.to_parquet(
            buffer,
            engine="pyarrow",
            index=False,
        )

        buffer.seek(0)

        try:

            s3_client.put_object(
                Bucket=settings.DATA_LAKE_BUCKET,
                Key=key,
                Body=buffer.getvalue(),
            )

            logger.success(
                f"Gold dataset uploaded to {key}"
            )

            self.metadata.update_dataset(
                dataset_name=f"{self.dataset_name}_gold",
                pipeline="silver_to_gold",
                layer="gold",
                last_file=key,
                rows_processed=len(df),
                status="SUCCESS",
                file_format="parquet",
            )

            logger.success(
                "Gold metadata updated successfully."
            )

        except Exception:
            logger.exception(
                "Failed to upload Gold dataset."
            )
            raise

        return key
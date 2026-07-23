import json
from datetime import datetime
from io import BytesIO

import pandas as pd

from config.logger import logger
from config.settings import settings
from quality.schema_validator import SchemaValidator
from schemas.products_schema import EXPECTED_COLUMNS
from utils.metadata_manager import MetadataManager
from utils.s3_client import s3_client


class BronzeToSilverService:

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.metadata = MetadataManager()

    def read_latest_bronze(self):

        key = self.metadata.get_last_file(self.dataset_name)

        logger.info(f"Reading {key}")

        response = s3_client.get_object(
            Bucket=settings.DATA_LAKE_BUCKET,
            Key=key
        )

        data = json.loads(
            response["Body"].read().decode("utf-8")
        )

        return pd.DataFrame(data)

    def clean_data(self, df):

        logger.info("Cleaning data...")

        # Remove duplicate products
        df = df.drop_duplicates(subset=["id"])

        # Remove rows with missing required fields
        df = df.dropna(
            subset=[
                "id",
                "title",
                "price"
            ]
        )

        # Convert data types
        df["id"] = df["id"].astype(int)
        df["price"] = df["price"].astype(float)

        # Flatten nested rating column
        logger.info("Flattening rating column...")

        df["rating_rate"] = df["rating"].apply(
            lambda x: x.get("rate") if isinstance(x, dict) else None
        )

        df["rating_count"] = df["rating"].apply(
            lambda x: x.get("count") if isinstance(x, dict) else None
        )

        # Convert rating columns to numeric
        df["rating_rate"] = pd.to_numeric(
            df["rating_rate"],
            errors="coerce"
        )

        df["rating_count"] = pd.to_numeric(
            df["rating_count"],
            errors="coerce"
        )

        # Remove original nested column
        df = df.drop(columns=["rating"])

        logger.info(f"Rows after cleaning: {len(df)}")

        # Validate schema
        SchemaValidator.validate_columns(
            df,
            EXPECTED_COLUMNS
        )

        return df

    def save_to_silver(self, df):

        logger.info("Writing Parquet file...")

        now = datetime.utcnow()

        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        timestamp = now.strftime("%Y%m%d_%H%M%S")

        key = (
            f"silver/{self.dataset_name}/"
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
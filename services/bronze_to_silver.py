from datetime import datetime, UTC

import pandas as pd

from config.logger import logger
from quality.validator import DataValidator
from services.s3_service import S3Service
from utils.metadata_manager import MetadataManager


class BronzeToSilverService:
    """
    Converts the latest Bronze JSON dataset into
    a cleaned Silver Parquet dataset.
    """

    def __init__(self, dataset_name: str = "products"):
        self.dataset_name = dataset_name
        self.s3 = S3Service()
        self.metadata = MetadataManager()

    def read_latest_bronze(self) -> pd.DataFrame:
        """
        Read latest Bronze JSON using metadata.
        """

        latest_file = self.metadata.get_last_file(
            self.dataset_name
        )

        logger.info(
            f"Reading Bronze file: {latest_file}"
        )

        data = self.s3.read_json(latest_file)

        return pd.DataFrame(data)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform Bronze data into Silver.
        """

        logger.info(
            "Starting Silver transformation..."
        )

        df = df.copy()

        # -----------------------------
        # Flatten nested rating object
        # -----------------------------
        if "rating" in df.columns:

            df["review_count"] = df["rating"].apply(
                lambda x: x.get("count", 0)
                if isinstance(x, dict)
                else 0
            )

            df["rating"] = df["rating"].apply(
                lambda x: x.get("rate", 0)
                if isinstance(x, dict)
                else 0
            )

        # -----------------------------
        # Remove duplicates
        # -----------------------------
        before = len(df)

        df = df.drop_duplicates(
            subset=["id"]
        )

        after = len(df)

        logger.info(
            f"Removed {before - after} duplicate rows."
        )

        # -----------------------------
        # Fill missing values
        # -----------------------------
        if "rating" in df.columns:
            df["rating"] = df["rating"].fillna(0)

        if "review_count" in df.columns:
            df["review_count"] = (
                df["review_count"].fillna(0)
            )

        logger.success(
            "Silver transformation completed."
        )

        return df

    def save(self, df: pd.DataFrame) -> str:
        """
        Save transformed data to Silver.
        """

        now = datetime.now(UTC)

        key = (
            f"silver/{self.dataset_name}/"
            f"year={now.year}/"
            f"month={now.month:02d}/"
            f"day={now.day:02d}/"
            f"{self.dataset_name}.parquet"
        )

        self.s3.write_parquet(
            df,
            key,
        )

        logger.success(
            f"Silver data written to {key}"
        )

        return key

    def run(self):
        """
        Execute Bronze → Silver pipeline.
        """

        try:

            logger.info(
                "Starting Bronze → Silver pipeline..."
            )

            # -----------------------------
            # Incremental Processing
            # -----------------------------
            latest_file = self.metadata.get_last_file(
                self.dataset_name
            )

            processed_file = (
                self.metadata.get_last_processed_file(
                    self.dataset_name
                )
            )

            logger.info(
                f"Latest Bronze file: {latest_file}"
            )

            logger.info(
                f"Last processed file: {processed_file}"
            )

            if latest_file == processed_file:

                logger.info(
                    "No new Bronze files found. "
                    "Skipping transformation."
                )

                return

            logger.info(
                "New Bronze file detected."
            )

            # -----------------------------
            # Read Bronze
            # -----------------------------
            df = self.read_latest_bronze()

            # -----------------------------
            # Transform
            # -----------------------------
            silver_df = self.transform(df)

            # -----------------------------
            # Validate Silver dataset
            # -----------------------------
            DataValidator.validate_dataframe(
                silver_df
            )

            DataValidator.validate_duplicate_ids(
                silver_df
            )

            DataValidator.validate_price(
                silver_df
            )

            DataValidator.validate_rating(
                silver_df
            )

            # -----------------------------
            # Save Silver
            # -----------------------------
            output_file = self.save(
                silver_df
            )

            # -----------------------------
            # Update Silver metadata
            # -----------------------------
            self.metadata.update_dataset(
                dataset_name=f"{self.dataset_name}_silver",
                pipeline="bronze_to_silver",
                layer="silver",
                last_file=output_file,
                rows_processed=len(silver_df),
                status="SUCCESS",
                file_format="parquet",
            )

            # -----------------------------
            # Mark Bronze file as processed
            # -----------------------------
            self.metadata.update_last_processed_file(
                self.dataset_name,
                latest_file,
            )

            logger.success(
                "Bronze → Silver pipeline completed successfully."
            )

        except Exception as e:

            logger.exception(
                "Bronze → Silver pipeline failed."
            )

            self.metadata.update_dataset(
                dataset_name=f"{self.dataset_name}_silver",
                pipeline="bronze_to_silver",
                layer="silver",
                last_file="",
                rows_processed=0,
                status=f"FAILED - {str(e)}",
                file_format="parquet",
            )

            raise
from config.logger import logger
import pandas as pd


class DataValidator:

    

    @staticmethod
    def validate_not_empty(data):

        if not data:
            raise ValueError("Dataset is empty.")

        logger.info("Dataset is not empty.")

    @staticmethod
    def validate_is_list(data):

        if not isinstance(data, list):
            raise TypeError("API response must be a list.")

        logger.info("Dataset is a list.")

    @staticmethod
    def validate_required_fields(data, required_fields):

        for record in data:

            missing = [
                field
                for field in required_fields
                if field not in record
            ]

            if missing:
                raise ValueError(f"Missing fields: {missing}")

        logger.info("Required fields validated.")

   

    @staticmethod
    def validate_dataframe(df: pd.DataFrame):

        if df.empty:
            raise ValueError("DataFrame is empty.")

        logger.info("DataFrame is not empty.")

    @staticmethod
    def validate_duplicate_ids(df: pd.DataFrame):

        if not df["id"].is_unique:
            raise ValueError("Duplicate product IDs found.")

        logger.info("No duplicate IDs found.")

    @staticmethod
    def validate_price(df: pd.DataFrame):

        if (df["price"] <= 0).any():
            raise ValueError("Price must be greater than zero.")

        logger.info("Price validation passed.")

    @staticmethod
    def validate_rating(df: pd.DataFrame):

        if (~df["rating"].between(0, 5)).any():
            raise ValueError("Invalid ratings found.")

        logger.info("Rating validation passed.")
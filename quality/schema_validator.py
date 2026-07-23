from config.logger import logger


class SchemaValidator:

    @staticmethod
    def validate_columns(df, expected_columns):

        actual_columns = list(df.columns)

        missing = [
            col
            for col in expected_columns
            if col not in actual_columns
        ]

        extra = [
            col
            for col in actual_columns
            if col not in expected_columns
        ]

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

        if extra:
            logger.warning(
                f"Extra columns detected: {extra}"
            )

        logger.info("Schema validation passed.")
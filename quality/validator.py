from config.logger import logger


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
                raise ValueError(
                    f"Missing fields: {missing}"
                )

        logger.info("Required fields validated.")
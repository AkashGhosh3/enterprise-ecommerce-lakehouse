from config.logger import logger
from services.bronze_to_silver import BronzeToSilverService


def main():
    logger.info("Starting Bronze → Silver transformation...")

    service = BronzeToSilverService("products")
    service.run()

    logger.success("Bronze → Silver transformation completed successfully.")


if __name__ == "__main__":
    main()
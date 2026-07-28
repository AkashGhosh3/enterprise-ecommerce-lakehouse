from config.logger import logger
from services.silver_to_gold import SilverToGoldService


def main():

    logger.info("Starting Silver → Gold transformation...")

    service = SilverToGoldService("products")

    df = service.read_latest_silver()

    gold_df = service.create_product_summary(df)

    logger.info(
        f"Gold dataset contains {gold_df.shape[0]} rows "
        f"and {gold_df.shape[1]} columns."
    )

    gold_key = service.save_to_gold(gold_df)

    logger.success("Silver → Gold completed successfully.")

    logger.info(f"Gold dataset saved to: {gold_key}")


if __name__ == "__main__":
    main()
from services.bronze_to_silver import BronzeToSilverService
from services.silver_to_gold import SilverToGoldService

bronze_service = BronzeToSilverService("products")

# Read Bronze data
df = bronze_service.read_latest_bronze()

# Transform to Silver
silver_df = bronze_service.clean_data(df)

# Create Gold summary
gold_service = SilverToGoldService("products")

summary_df = gold_service.create_product_summary(
    silver_df
)

print(summary_df)

# Upload Gold dataset
gold_service.save_to_gold(summary_df)
from services.bronze_to_silver import BronzeToSilverService

service = BronzeToSilverService("products")

df = service.read_latest_bronze()

clean_df = service.clean_data(df)

print(clean_df.head())

print(clean_df.columns)

print(clean_df.dtypes)

service.save_to_silver(clean_df)

print(clean_df.shape)
from config.data_sources import DATA_SOURCES
from ingestion.api_ingestion import APIIngestion

config = DATA_SOURCES["products"]

pipeline = APIIngestion(
    api_url=config["url"],
    dataset_name="products"
)

data = pipeline.extract()
pipeline.save(data)
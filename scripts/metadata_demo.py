from utils.metadata_manager import MetadataManager

manager = MetadataManager()

manager.update_dataset(
    dataset_name="products",
    layer="bronze",
    last_file="bronze/products/test.json",
    rows=20,
    status="SUCCESS",
    file_format="json"
)

print(manager.get_dataset_metadata("products"))
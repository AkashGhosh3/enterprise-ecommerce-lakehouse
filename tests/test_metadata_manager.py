from utils.metadata_manager import MetadataManager


def test_write_and_read_metadata(tmp_path):

    metadata_file = tmp_path / "metadata.json"

    manager = MetadataManager()
    manager.metadata_file = metadata_file

    sample = {
        "products": {
            "last_file": "bronze/file.json"
        }
    }

    manager.write_metadata(sample)

    result = manager.read_metadata()

    assert result == sample


def test_update_dataset(tmp_path):

    metadata_file = tmp_path / "metadata.json"

    manager = MetadataManager()
    manager.metadata_file = metadata_file

    manager.update_dataset(
        dataset_name="products",
        layer="bronze",
        last_file="bronze/file.json",
        rows_processed=20,
    )

    metadata = manager.read_metadata()

    assert "products" in metadata
    assert metadata["products"]["last_file"] == "bronze/file.json"
    assert metadata["products"]["rows_processed"] == 20
    assert metadata["products"]["status"] == "SUCCESS"


def test_get_last_file(tmp_path):

    metadata_file = tmp_path / "metadata.json"

    manager = MetadataManager()
    manager.metadata_file = metadata_file

    manager.write_metadata(
        {
            "products": {
                "last_file": "bronze/test.json"
            }
        }
    )

    assert (
        manager.get_last_file("products")
        == "bronze/test.json"
    )


def test_update_last_processed_file(tmp_path):

    metadata_file = tmp_path / "metadata.json"

    manager = MetadataManager()
    manager.metadata_file = metadata_file

    manager.write_metadata(
        {
            "products": {}
        }
    )

    manager.update_last_processed_file(
        "products",
        "bronze/file.json",
    )

    assert (
        manager.get_last_processed_file("products")
        == "bronze/file.json"
    )


def test_get_dataset_metadata(tmp_path):

    metadata_file = tmp_path / "metadata.json"

    manager = MetadataManager()
    manager.metadata_file = metadata_file

    manager.write_metadata(
        {
            "products": {
                "status": "SUCCESS"
            }
        }
    )

    metadata = manager.get_dataset_metadata(
        "products"
    )

    assert metadata["status"] == "SUCCESS"
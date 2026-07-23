from importlib import metadata
import json
from pathlib import Path

from config.logger import logger


class MetadataManager:

    def __init__(self):
        self.metadata_file = Path(
            "metadata/ingestion_metadata.json"
        )

    def read_metadata(self):

        if not self.metadata_file.exists():
            return {}

        with open(self.metadata_file, "r") as file:
            return json.load(file)

    def write_metadata(self, metadata):

        with open(self.metadata_file, "w") as file:
            json.dump(
                metadata,
                file,
                indent=4
            )

        logger.info("Metadata updated successfully.")

    def get_last_file(self, dataset_name):

        metadata = self.read_metadata()

        dataset = metadata.get(dataset_name)

        if not dataset:
            raise ValueError(
                f"No metadata found for dataset '{dataset_name}'."
            )

        return dataset["last_file"]
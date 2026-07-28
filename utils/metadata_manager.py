import json
from datetime import datetime, UTC
from pathlib import Path

from config.logger import logger


class MetadataManager:

    def __init__(self):
        self.metadata_file = Path(
            "metadata/ingestion_metadata.json"
        )

    def read_metadata(self):
        """
        Read metadata from JSON file.
        """

        if not self.metadata_file.exists():
            return {}

        with open(self.metadata_file, "r") as file:
            return json.load(file)

    def write_metadata(self, metadata):
        """
        Write metadata to JSON file.
        """

        self.metadata_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(self.metadata_file, "w") as file:
            json.dump(
                metadata,
                file,
                indent=4,
            )

        logger.info("Metadata updated successfully.")

    def update_dataset(
        self,
        dataset_name,
        layer,
        last_file,
        rows_processed,
        status="SUCCESS",
        pipeline="enterprise_ecommerce_pipeline",
        file_format="json",
    ):
        """
        Update dataset metadata.
        """

        metadata = self.read_metadata()

        existing = metadata.get(dataset_name, {})

        metadata[dataset_name] = {
            "pipeline": pipeline,
            "layer": layer,
            "last_file": last_file,

            # Preserve previously processed file
            "last_processed_file": existing.get(
                "last_processed_file",
                "",
            ),

            "rows_processed": rows_processed,
            "status": status,
            "file_format": file_format,
            "last_updated": datetime.now(
                UTC
            ).isoformat(),
        }

        self.write_metadata(metadata)

    def get_last_file(self, dataset_name):
        """
        Return latest file for dataset.
        """

        metadata = self.read_metadata()

        dataset = metadata.get(dataset_name)

        if not dataset:
            raise ValueError(
                f"No metadata found for '{dataset_name}'."
            )

        return dataset["last_file"]

    def get_last_processed_file(
        self,
        dataset_name,
    ):
        """
        Return last processed Bronze file.
        """

        metadata = self.read_metadata()

        dataset = metadata.get(dataset_name)

        if not dataset:
            return ""

        return dataset.get(
            "last_processed_file",
            "",
        )

    def update_last_processed_file(
        self,
        dataset_name,
        file_key,
    ):
        """
        Update last processed Bronze file.
        """

        metadata = self.read_metadata()

        if dataset_name not in metadata:
            metadata[dataset_name] = {}

        metadata[dataset_name][
            "last_processed_file"
        ] = file_key

        metadata[dataset_name][
            "last_updated"
        ] = datetime.now(
            UTC
        ).isoformat()

        self.write_metadata(metadata)

        logger.success(
            f"Updated last processed file for '{dataset_name}'."
        )

    def get_dataset_metadata(
        self,
        dataset_name,
    ):
        """
        Return complete metadata for dataset.
        """

        metadata = self.read_metadata()

        if dataset_name not in metadata:
            raise ValueError(
                f"No metadata found for '{dataset_name}'."
            )

        return metadata[dataset_name]
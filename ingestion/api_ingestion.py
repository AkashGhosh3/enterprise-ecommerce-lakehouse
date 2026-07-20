from importlib.metadata import metadata
import json
from datetime import datetime
from quality.validator import DataValidator
import requests
from utils.metadata_manager import MetadataManager
from config.logger import logger
from config.settings import settings
from ingestion.base_ingestion import BaseIngestion
from utils.s3_client import s3_client


class APIIngestion(BaseIngestion):

    def __init__(self, api_url: str, dataset_name: str):
        self.api_url = api_url
        self.dataset_name = dataset_name

    def extract(self):
        logger.info(f"Fetching data from {self.api_url}")

        response = requests.get(self.api_url)

        response.raise_for_status()

        data = response.json()

        DataValidator.validate_not_empty(data)

        DataValidator.validate_is_list(data)

        DataValidator.validate_required_fields(
            data,
            [
                "id",
                "title",
                "price"
            ]
        )

        return data

    def save(self, data):

        now = datetime.utcnow()

        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        timestamp = now.strftime("%Y%m%d_%H%M%S")

        key = (
            f"bronze/{self.dataset_name}/"
            f"year={year}/"
            f"month={month}/"
            f"day={day}/"
            f"{timestamp}.json"
        )

        s3_client.put_object(
            Bucket=settings.DATA_LAKE_BUCKET,
            Key=key,
            Body=json.dumps(data)
        )

        logger.success(f"Uploaded {key}")
        manager = MetadataManager()

        metadata = manager.read_metadata()

        metadata[self.dataset_name] = {
            "last_run": datetime.utcnow().isoformat(),
            "last_file": key
}

        manager.write_metadata(metadata)
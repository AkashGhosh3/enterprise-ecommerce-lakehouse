from io import BytesIO
import json

import pandas as pd

from config.settings import settings
from utils.s3_client import s3_client


class S3Service:

    def read_json(self, key):

        response = s3_client.get_object(
            Bucket=settings.S3_BUCKET,
            Key=key,
        )

        return json.loads(
            response["Body"].read().decode("utf-8")
        )

    def write_parquet(self, df, key):

        buffer = BytesIO()

        df.to_parquet(buffer, index=False)

        s3_client.put_object(
            Bucket=settings.S3_BUCKET,
            Key=key,
            Body=buffer.getvalue(),
        )
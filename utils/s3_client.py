import boto3

from config.settings import settings


class S3Client:

    def __init__(self):
        self.client = boto3.client(
            "s3",
            region_name=settings.AWS_REGION
        )


s3_client = S3Client().client
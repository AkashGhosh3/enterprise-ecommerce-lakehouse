from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    AWS_REGION = os.getenv("AWS_REGION")
    PROJECT_NAME = os.getenv("PROJECT_NAME")
    DATA_LAKE_BUCKET = os.getenv("DATA_LAKE_BUCKET")
    ATHENA_DATABASE = os.getenv("ATHENA_DATABASE")


settings = Settings()
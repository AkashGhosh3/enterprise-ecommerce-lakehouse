from utils.s3_client import s3_client

print("Connected to AWS")

response = s3_client.list_buckets()

print(response)
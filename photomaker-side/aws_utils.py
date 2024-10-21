import os
from dotenv import load_dotenv
import boto3

# Load environment variables from .env file
load_dotenv()


def upload_to_s3(s3_client, file_path, job_id, domain_name, bucket_name, key_path):
  """Upload the final edited video to Cloud Storage (S3 bucket)"""
  key = f"{key_path}{job_id}"
  s3_client.upload_file(file_path, bucket_name, key, ExtraArgs={'ContentType':f'image/{job_id.split(".")[-1]}','ContentDisposition': f'attachment; filename={job_id}' })
  return f"{domain_name}/{key}"

def Initialize_s3():
  """Initialize the S3 bucket"""
  AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
  AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
  s3_client = boto3.client("s3",aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
  return s3_client
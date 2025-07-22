import boto3
from botocore.exceptions import ClientError
import os
import argparse


# Parse command-line argument
parser = argparse.ArgumentParser(description='Use S3 API with MinIO.')
parser.add_argument('endpoint', help='MinIO endpoint URL')
args = parser.parse_args()

# Step 1: Create test file
with open('example-python.txt', 'w') as f:
    f.write('Hello from MinIO! This is a test file made in python.\n')

# Step 2: Connect to MinIO
# region_name must be us-east-1
minio_pw = os.getenv("MINIO_PW", "minioadmin")
s3 = boto3.client('s3',
                  endpoint_url=args.endpoint,
                  aws_access_key_id='minioadmin',
                  aws_secret_access_key=minio_pw,
                  region_name='us-east-1')

bucket_name = 'my-python-bucket'
object_name = 'example-python.txt'

# Step 3: Create bucket (ignore error if already exists)
try:
    s3.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created successfully.")
except ClientError as e:
    if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
        print(f"Bucket '{bucket_name}' already exists.")
    else:
        raise

# Step 4: Upload the file
s3.upload_file('example-python.txt', bucket_name, object_name)
print(f"Uploaded '{object_name}' to bucket '{bucket_name}'.")

# Step 5: Download the file
s3.download_file(bucket_name, object_name, 'debug/downloaded-python-test.txt')
print(f"Downloaded '{object_name}' to 'debug/downloaded-python-test.txt'.")

# Step 6: Delete the file from the bucket
#s3.delete_object(Bucket=bucket_name, Key=object_name)
#print(f"Deleted '{object_name}' from bucket '{bucket_name}'.")

#!/usr/bin/env python3
"""
MinIO File Organizer
Moves files into organized folders within MinIO bucket.
"""

import boto3
from botocore.client import Config
import os
import sys
from urllib.parse import urlparse, unquote
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MinIO configuration
MINIO_ENDPOINT = os.getenv('S3_ENDPOINT_URL', 'http://minio:9000')
MINIO_ACCESS_KEY = os.getenv('S3_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.getenv('S3_SECRET_KEY', 'minioadmin')
MINIO_BUCKET = os.getenv('S3_BUCKET_NAME', 'nca-toolkit')

# Initialize S3 client
s3_client = boto3.client(
    's3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

def parse_minio_url(url):
    """
    Parse MinIO URL and extract bucket and key.
    Example: http://minio:9000/nca-toolkit/file.mp4 -> ('nca-toolkit', 'file.mp4')
    """
    parsed = urlparse(url)
    path_parts = parsed.path.lstrip('/').split('/', 1)
    if len(path_parts) == 2:
        # URL decode the key to get the actual filename in MinIO
        return path_parts[0], unquote(path_parts[1])
    return MINIO_BUCKET, unquote(path_parts[0])

def move_file(source_key, dest_key, bucket=MINIO_BUCKET):
    """
    Move a file within MinIO by copying and deleting the original.
    """
    try:
        # Copy the file
        copy_source = {'Bucket': bucket, 'Key': source_key}
        s3_client.copy_object(
            CopySource=copy_source,
            Bucket=bucket,
            Key=dest_key
        )
        logger.info(f"Copied: {source_key} -> {dest_key}")
        
        # Delete the original
        s3_client.delete_object(Bucket=bucket, Key=source_key)
        logger.info(f"Deleted original: {source_key}")
        
        return True
    except Exception as e:
        logger.error(f"Failed to move {source_key}: {e}")
        return False

def organize_all_root_files(execution_folder, bucket=MINIO_BUCKET):
    """
    Organize ALL files at the root of the bucket into an execution folder.
    This scans the bucket and moves any file that's not already in a folder.

    Args:
        execution_folder: Name of the folder to organize files into
        bucket: MinIO bucket name

    Returns:
        List of new URLs after organization
    """
    new_urls = []

    try:
        # List all objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket)

        if 'Contents' not in response:
            logger.info("No files found in bucket")
            return new_urls

        for obj in response['Contents']:
            source_key = obj['Key']

            # Skip if it's already in a folder (contains /)
            if '/' in source_key:
                continue

            # Skip if it's the execution folder itself
            if source_key == execution_folder or source_key == execution_folder + '/':
                continue

            # Get filename
            filename = os.path.basename(source_key)

            # Create destination key
            dest_key = f"{execution_folder}/{filename}"

            # Move the file
            if move_file(source_key, dest_key, bucket):
                new_url = f"{MINIO_ENDPOINT}/{bucket}/{dest_key}"
                new_urls.append(new_url)
                logger.info(f"Organized: {source_key} -> {dest_key}")

    except Exception as e:
        logger.error(f"Error listing bucket: {e}")

    return new_urls

def organize_files(execution_folder, file_urls):
    """
    Organize files into an execution folder.

    Args:
        execution_folder: Name of the folder to organize files into
        file_urls: List of MinIO URLs to organize

    Returns:
        List of new URLs after organization
    """
    new_urls = []

    for url in file_urls:
        try:
            bucket, source_key = parse_minio_url(url)

            # Skip if already in a folder
            if source_key.startswith(execution_folder + '/'):
                logger.info(f"File already in folder: {source_key}")
                new_urls.append(url)
                continue

            # Get filename from source key
            filename = os.path.basename(source_key)

            # Create destination key
            dest_key = f"{execution_folder}/{filename}"

            # Move the file
            if move_file(source_key, dest_key, bucket):
                new_url = f"{MINIO_ENDPOINT}/{bucket}/{dest_key}"
                new_urls.append(new_url)
                logger.info(f"Organized: {url} -> {new_url}")
            else:
                new_urls.append(url)  # Keep original if move failed

        except Exception as e:
            logger.error(f"Error processing {url}: {e}")
            new_urls.append(url)  # Keep original if error

    return new_urls

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: organize.py <execution_folder> <file_url1> [file_url2] ...")
        sys.exit(1)
    
    execution_folder = sys.argv[1]
    file_urls = sys.argv[2:]
    
    logger.info(f"Organizing {len(file_urls)} files into folder: {execution_folder}")
    new_urls = organize_files(execution_folder, file_urls)
    
    print("\n=== Organized Files ===")
    for url in new_urls:
        print(url)
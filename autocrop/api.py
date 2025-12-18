#!/usr/bin/env python3
"""
Simple HTTP API wrapper for the autocrop script.
Allows n8n to call the autocrop functionality via HTTP requests.
Supports MinIO for input/output file handling.
"""

from flask import Flask, request, jsonify
import subprocess
import os
import uuid
import logging
import boto3
from botocore.client import Config
import tempfile
from urllib.parse import urlparse

app = Flask(__name__)
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
        return path_parts[0], path_parts[1]
    return MINIO_BUCKET, path_parts[0]

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "autocrop", "minio": MINIO_ENDPOINT}), 200

@app.route('/convert', methods=['POST'])
def convert_video():
    """
    Convert horizontal video to vertical format.

    Expected JSON body:
    {
        "input_url": "http://minio:9000/nca-toolkit/video_split_1.mp4",
        "output_key": "video_vertical.mp4"  (optional, defaults to input_key with _vertical suffix)
    }

    Returns:
    {
        "success": true,
        "output_url": "http://minio:9000/nca-toolkit/video_vertical.mp4",
        "message": "Video converted successfully"
    }
    """
    temp_input = None
    temp_output = None

    try:
        data = request.get_json()

        if not data or 'input_url' not in data:
            return jsonify({
                "success": False,
                "error": "Missing required field: input_url"
            }), 400

        input_url = data['input_url']

        # Parse MinIO URL
        bucket, input_key = parse_minio_url(input_url)
        logger.info(f"Downloading from MinIO: bucket={bucket}, key={input_key}")

        # Create temporary files
        temp_input = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        temp_output = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        temp_input.close()
        temp_output.close()
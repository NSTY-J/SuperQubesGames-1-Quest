#!/usr/bin/env python3
"""
MinIO File Organizer API
HTTP API wrapper for organizing files in MinIO.
"""

from flask import Flask, request, jsonify
import logging
from organize import organize_files, MINIO_ENDPOINT

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "minio-organizer",
        "minio": MINIO_ENDPOINT
    }), 200

@app.route('/organize', methods=['POST'])
def organize():
    """
    Organize files into a folder in MinIO.
    
    Expected JSON body:
    {
        "execution_folder": "execution_2025-11-01_abc123",
        "file_urls": [
            "http://minio:9000/nca-toolkit/file1.mp4",
            "http://minio:9000/nca-toolkit/file2.mp3"
        ]
    }
    
    Returns:
    {
        "success": true,
        "execution_folder": "execution_2025-11-01_abc123",
        "organized_files": [
            "http://minio:9000/nca-toolkit/execution_2025-11-01_abc123/file1.mp4",
            "http://minio:9000/nca-toolkit/execution_2025-11-01_abc123/file2.mp3"
        ],
        "count": 2
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'execution_folder' not in data or 'file_urls' not in data:
            return jsonify({
                "success": False,
                "error": "Missing required fields: execution_folder, file_urls"
            }), 400
        
        execution_folder = data['execution_folder']
        file_urls = data['file_urls']
        
        if not isinstance(file_urls, list):
            return jsonify({
                "success": False,
                "error": "file_urls must be an array"
            }), 400
        
        logger.info(f"Organizing {len(file_urls)} files into folder: {execution_folder}")
        
        # Organize the files
        organized_urls = organize_files(execution_folder, file_urls)
        
        return jsonify({
            "success": True,
            "execution_folder": execution_folder,
            "organized_files": organized_urls,
            "count": len(organized_urls)
        }), 200
        
    except Exception as e:
        logger.exception("Error organizing files")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084, debug=False)
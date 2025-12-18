#!/bin/bash
# Create required directories for docker-compose bind mounts

mkdir -p n8n
mkdir -p minio/data
mkdir -p ffmpeg/files/clips
mkdir -p ffmpeg/files/jobs
mkdir -p FINAL/YT_Clips

# Create .gitkeep files to preserve directory structure in git
touch ffmpeg/files/.gitkeep
touch ffmpeg/files/jobs/.gitkeep
touch FINAL/YT_Clips/.gitkeep

echo "Directories created successfully!"


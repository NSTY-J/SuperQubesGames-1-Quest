FROM python:3.11-slim

# Install system dependencies with BuildKit cache
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install CPU-only torch first (much smaller than CUDA version ~150MB vs ~900MB)
# This saves significant download time for users with slow internet
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --timeout=1000 --retries=5 \
    --index-url https://download.pytorch.org/whl/cpu \
    torch

# Copy requirements and install remaining Python dependencies
# Use BuildKit cache mount for faster pip installs on subsequent builds
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --timeout=1000 --retries=5 -r requirements.txt

# Copy the scripts
COPY main.py .
COPY api.py .

# Create directory for YOLO models
RUN mkdir -p /root/.cache/torch/hub/checkpoints

# Expose API port
EXPOSE 8083

# Set entrypoint to run the API server
ENTRYPOINT ["python", "api.py"]
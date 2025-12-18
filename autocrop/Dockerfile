FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
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

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scripts
COPY main.py .
COPY api.py .

# Create directory for YOLO models
RUN mkdir -p /root/.cache/torch/hub/checkpoints

# Expose API port
EXPOSE 8083

# Set entrypoint to run the API server
ENTRYPOINT ["python", "api.py"]
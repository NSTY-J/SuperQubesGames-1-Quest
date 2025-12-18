FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY organize.py .
COPY api.py .

# Expose port
EXPOSE 8084

# Run the API server
CMD ["python", "api.py"]
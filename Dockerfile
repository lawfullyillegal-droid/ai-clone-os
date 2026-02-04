# ENS Legis AI Clone OS
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add Flask to requirements if not present
RUN pip install --no-cache-dir flask gunicorn

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/config

# Set environment variables
ENV FLASK_APP=dashboard.py
ENV PYTHONUNBUFFERED=1

# Expose port for dashboard
EXPOSE 5000

# Health check using curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/status || exit 1

# Run dashboard by default
CMD ["python", "dashboard.py"]

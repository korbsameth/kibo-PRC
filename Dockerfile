# Dockerfile for kibo-PRC Autonomous Navigation System
# Kibo-RPC (Robot Programming Challenge) - Int-Ball2 Control System

FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency definition
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY code/ ./code/
COPY tests/ ./tests/

# Set Python path to find modules inside code/
ENV PYTHONPATH="/app/code:${PYTHONPATH}"

# Default command: execute the autonomous mission
CMD ["python", "code/main.py"]

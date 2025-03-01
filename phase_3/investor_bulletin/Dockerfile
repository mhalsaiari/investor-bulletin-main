FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies first
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*


# Copy requirements
COPY requirements.txt /app/requirements.txt

# Install Python packages
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app/

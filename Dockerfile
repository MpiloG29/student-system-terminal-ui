FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for persistent storage
RUN mkdir -p /app/data


EXPOSE 5000

# Default to web runtime so Render Web Services stay alive.
# For one-off ETL runs, override command: python run_pipeline.py 1
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} web_app:app"]
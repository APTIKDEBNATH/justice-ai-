# Justice AI - Production Container
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose backend (5000), frontend (3000), and streamlit (8501)
EXPOSE 5000 3000 8501

# Default command starts the unified orchestrator
CMD ["python", "run_all.py"]

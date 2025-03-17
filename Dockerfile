FROM python:3.12.6-slim

WORKDIR /app

# Install system dependencies, PostgreSQL client, and uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Use the --system flag with uv since we're not using a virtual environment
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Command will be overridden by docker-compose
CMD ["python", "-m", "src.backend"]
FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY src/ src/
COPY config.yaml .

# Install the package
RUN pip install --no-cache-dir .

# Create data directory
RUN mkdir -p /data

# Expose web UI port
EXPOSE 8000

# Default: start the web dashboard
ENV PYREVIEW_DB_PATH=/data/reviews.db
CMD ["pyreview", "serve", "--host", "0.0.0.0", "--port", "8000"]

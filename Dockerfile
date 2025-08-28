# ---------------------------
# Base image
# ---------------------------
FROM python:3.10-slim

# Avoid Python buffering issues
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# ---------------------------
# Install system dependencies
# ---------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       gcc \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------
# Install Python dependencies first
# to maximize Docker build cache usage
# ---------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---------------------------
# Copy project files
# ---------------------------
COPY . .

# ---------------------------
# Create static/media dirs with proper permissions
# ---------------------------
RUN mkdir -p /app/staticfiles /app/mediafiles \
    && chown -R root:root /app/staticfiles /app/mediafiles

# ---------------------------
# Collect static files
# (ensure Django settings are ready for prod)
# ---------------------------
RUN python manage.py collectstatic --noinput

# ---------------------------
# Run Gunicorn by default
# ---------------------------
CMD ["gunicorn", "server.wsgi:application", "--bind", "0.0.0.0:8000"]

# ---------------------------
# Base image
# ---------------------------
FROM python:3.10-slim-bookworm

# ---------------------------
# Environment settings
# ---------------------------
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# ---------------------------
# Install system dependencies
# ---------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       libpq5 \
       gcc \
       postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------
# Install Python dependencies
# ---------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---------------------------
# Copy project files
# ---------------------------
COPY . .

# ---------------------------
# Prepare static/media directories
# ---------------------------
RUN mkdir -p /app/staticfiles /app/mediafiles \
    && chown -R root:root /app/staticfiles /app/mediafiles

# ---------------------------
# Collect static files
# ---------------------------
RUN python manage.py collectstatic --noinput

# ---------------------------
# Start Gunicorn server
# ---------------------------
CMD ["gunicorn", "server.wsgi:application", "--bind", "0.0.0.0:8000"]

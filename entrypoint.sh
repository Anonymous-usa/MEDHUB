#!/bin/bash
set -e

echo "🔍 Validating environment..."
if [ -z "$DJANGO_SECRET_KEY" ]; then
  echo "❌ .env not loaded. Aborting startup."
  exit 1
fi

echo "⏳ Waiting for PostgreSQL to be ready..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER"; do
  sleep 2
done

echo "🔧 Running makemigrations and migrate..."
python manage.py makemigrations
python manage.py migrate

echo "📞 Creating phone-based superuser if not exists..."
python manage.py shell < /app/scripts/create_superuser.py

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn..."
exec gunicorn server.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 120 \
    --log-level info \
    --access-logfile -

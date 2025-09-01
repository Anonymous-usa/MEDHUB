#!/bin/bash
set -e

echo "🔧 Running makemigrations and migrate..."
python manage.py makemigrations
python manage.py migrate

echo "📞 Creating phone-based superuser if not exists..."
DJANGO_SUPERUSER_PHONE=${DJANGO_SUPERUSER_PHONE:-+992900000001}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-adminpass}

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(phone='${DJANGO_SUPERUSER_PHONE}').exists():
    User.objects.create_superuser(
        phone='${DJANGO_SUPERUSER_PHONE}',
        password='${DJANGO_SUPERUSER_PASSWORD}'
    )
END

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

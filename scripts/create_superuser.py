from django.contrib.auth import get_user_model
import os

User = get_user_model()
phone = os.getenv("DJANGO_SUPERUSER_PHONE", "+992900000001")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "adminpass")

if not User.objects.filter(phone_number=phone).exists():
    User.objects.create_superuser(
        phone_number=phone,
        email="admin@medhub.tj",
        password=password
    )
    print(f"✅ Superuser created: {phone}")
else:
    print(f"ℹ️ Superuser already exists: {phone}")

# server/celery.py

import os
from celery import Celery

# Задаём настройки Django-проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')

# Загружаем конфигурацию Celery из настроек Django с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи (shared_task) в установленных приложениях
app.autodiscover_tasks()

# Dockerfile

FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Системные зависимости для сборки
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Копируем весь код проекта
COPY . .

# Собираем статику (если используешь collectstatic)
RUN python manage.py collectstatic --noinput

# Запуск Gunicorn
CMD ["gunicorn", "server.wsgi:application", "--bind", "0.0.0.0:8000"]


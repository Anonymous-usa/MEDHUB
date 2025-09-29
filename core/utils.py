import re
import uuid
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

TAJIK_PHONE_PREFIX = '+992'


def normalize_phone_number(phone_number: str) -> str:
    """
    Приводит номер к формату +992XXXXXXXXX.
    - Убирает пробелы, дефисы, скобки.
    - Локальный формат (0XXXXXXXXX) → международный (+992XXXXXXXXX).
    - Если номер уже в международном формате, возвращает как есть.
    """
    if not phone_number:
        return ""

    cleaned = re.sub(r'[\s\-\(\)]', '', str(phone_number))

    # Локальный формат: 0XXXXXXXXX (10 цифр)
    if cleaned.startswith('0') and len(cleaned) == 10:
        return f"{TAJIK_PHONE_PREFIX}{cleaned[1:]}"

    # Если уже начинается с +992
    if cleaned.startswith(TAJIK_PHONE_PREFIX):
        return cleaned

    # Если номер без +992, но длина 9 (например, 9XXXXXXXX)
    if len(cleaned) == 9 and cleaned.isdigit():
        return f"{TAJIK_PHONE_PREFIX}{cleaned}"

    return cleaned


def generate_unique_slug(instance, value: str, slug_field: str = 'slug') -> str:
    """
    Генерирует уникальный slug для модели.
    - Использует slugify для нормализации.
    - Если slug пустой → генерирует UUID.
    - Если slug уже существует, добавляет числовой суффикс.
    """
    base_slug = slugify(value) if value else str(uuid.uuid4())[:8]
    unique_slug = base_slug
    Model = instance.__class__
    counter = 1

    while Model.objects.filter(**{slug_field: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1

    return unique_slug

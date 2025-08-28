import re
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

TAJIK_PHONE_PREFIX = '+992'

def normalize_phone_number(phone_number: str) -> str:
    """
    Приводит номер к формату +992XXXXXXXXX.
    Убирает пробелы, дефисы, скобки и приводит локальный формат к международному.
    """
    cleaned = re.sub(r'[\s\-\(\)]', '', phone_number)
    if cleaned.startswith('0') and len(cleaned) == 10:
        return f"{TAJIK_PHONE_PREFIX}{cleaned[1:]}"
    return cleaned


def generate_unique_slug(instance, value, slug_field='slug') -> str:
    """
    Генерирует уникальный slug для модели.
    Если slug уже существует, добавляет числовой суффикс.
    """
    base_slug = slugify(value)
    unique_slug = base_slug
    Model = instance.__class__
    counter = 1

    while Model.objects.filter(**{slug_field: unique_slug}).exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1

    return unique_slug

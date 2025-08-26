import re
from django.utils.text import slugify

def normalize_phone_number(phone_number: str) -> str:
    """
    Приводит номер к формату +992XXXXXXXXX.
    """
    # Убираем пробелы, дефисы и скобки
    cleaned = re.sub(r'[\s\-\(\)]', '', phone_number)
    if cleaned.startswith('0') and len(cleaned) == 10:
        return '+992' + cleaned[1:]
    return cleaned

def generate_unique_slug(instance, value, slug_field='slug'):
    """
    Генерирует уникальный slug для моделей, имеющих поле slug.
    """
    base_slug = slugify(value)
    unique_slug = base_slug
    Model = instance.__class__
    counter = 1

    while Model.objects.filter(**{slug_field: unique_slug}).exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1

    return unique_slug

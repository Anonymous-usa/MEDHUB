import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

TAJIK_PHONE_PATTERN = r'^(\+992\d{9}|0\d{9})$'

def validate_phone_number(value: str):
    """
    Проверяет корректность таджикского номера телефона.
    Форматы:
    - +992XXXXXXXXX
    - 0XXXXXXXXX
    """
    normalized = re.sub(r'[\s\-\(\)]', '', value)
    if not re.match(TAJIK_PHONE_PATTERN, normalized):
        raise ValidationError(
            _('Номер телефона "%(value)s" некорректен. Используйте формат +992123456789 или 0123456789'),
            params={'value': value}
        )
    return value

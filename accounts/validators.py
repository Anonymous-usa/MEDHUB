import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

TAJIK_PHONE_PATTERN = r'^(\+992\d{9}|0\d{9})$'

def validate_phone_number(value):
    # Убираем лишние символы и проверяем по шаблону
    value = re.sub(r'[\s\-\(\)]', '', value)
    if not re.match(TAJIK_PHONE_PATTERN, value):
        raise ValidationError(
            _('Номер телефона "%(value)s" некорректен. Используйте формат +992123456789 или 0123456789'),
            params={'value': value}
        )
    return value

import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from accounts.validators import validate_phone_number

User = get_user_model()
logger = logging.getLogger(__name__)

class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        if phone_number is None or password is None:
            return None

        phone_number = validate_phone_number(phone_number)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            logger.warning(f"Пользователь не найден: {phone_number}")
            return None

        if not user.check_password(password):
            logger.warning(f"Неверный пароль для: {phone_number}")
            return None
        if not user.is_active:
            logger.warning(f"Аккаунт деактивирован: {phone_number}")
            return None
        if hasattr(user, 'is_verified') and not user.is_verified:
            logger.warning(f"Аккаунт не верифицирован: {phone_number}")
            return None

        logger.info(f"Аутентификация успешна: {user.phone_number}")
        return user

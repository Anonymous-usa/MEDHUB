import logging
from django.core.mail import send_mail
from django.conf import settings
from .utils import normalize_phone_number

logger = logging.getLogger(__name__)


def send_sms_task(phone_number: str, message: str) -> bool:
    """
    Фоновая задача для отправки SMS.
    Интеграция с конкретным провайдером SMS-шлюза должна быть реализована здесь.
    Возвращает True при успехе, False при ошибке.
    """
    try:
        normalized = normalize_phone_number(phone_number)
        # TODO: sms_gateway.send(normalized, message)
        logger.info(f"✅ SMS отправлено на {normalized}: {message}")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке SMS на {phone_number}: {e}")
        return False


def send_email_task(subject: str, body: str, recipient_list: list) -> bool:
    """
    Отправка email через Django Email backend.
    Возвращает True при успехе, False при ошибке.
    """
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipient_list)
        logger.info(f"✅ Email отправлен: {subject} → {recipient_list}")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке email ({subject} → {recipient_list}): {e}")
        return False


def send_push_task(user_id: int, title: str, message: str) -> bool:
    """
    Фоновая задача для отправки push-уведомлений.
    Реализацию адаптировать под выбранный push-сервис.
    Возвращает True при успехе, False при ошибке.
    """
    try:
        # TODO: push_service.send(user_id, title, message)
        logger.info(f"✅ Push-уведомление → user {user_id}: {title} — {message}")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке push-уведомления пользователю {user_id}: {e}")
        return False

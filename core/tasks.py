from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .utils import normalize_phone_number
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_sms_task(phone_number: str, message: str) -> bool:
    """
    Фоновая задача для отправки SMS.
    Интеграция с конкретным провайдером SMS-шлюза должна быть реализована здесь.
    """
    normalized = normalize_phone_number(phone_number)
    # TODO: sms_gateway.send(normalized, message)
    logger.info(f"SMS отправлено на {normalized}: {message}")
    return True


@shared_task
def send_email_task(subject: str, body: str, recipient_list: list) -> bool:
    """
    Отправка email через Django Email backend.
    """
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipient_list)
        logger.info(f"Email отправлен: {subject} → {recipient_list}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке email: {e}")
        return False


@shared_task
def send_push_task(user_id: int, title: str, message: str) -> None:
    """
    Фоновая задача для отправки push-уведомлений.
    Реализацию адаптировать под выбранный push-сервис.
    """
    # TODO: push_service.send(user_id, title, message)
    logger.info(f"Push-уведомление → user {user_id}: {title} — {message}")

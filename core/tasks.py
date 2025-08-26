from  celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .utils import normalize_phone_number

@shared_task
def send_sms_task(phone_number: str, message: str) -> bool:
    """
    Фоновая задача для отправки SMS.
    Интеграция с конкретным провайдером SMS-шлюза должна быть реализована здесь.
    """
    normalized = normalize_phone_number(phone_number)
    # Пример: sms_gateway.send(normalized, message)
    return True

@shared_task
def send_email_task(subject: str, body: str, recipient_list: list) -> bool:
    """
    Отправка email через Django Email backend.
    """
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipient_list)
    return True

@shared_task
def send_push_task(user_id: int, title: str, message: str) -> None:
    """
    Фоновая задача для отправки push-уведомлений.
    Реализацию адаптировать под выбранный push-сервис.
    """
    pass

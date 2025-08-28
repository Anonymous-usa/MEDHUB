# notification/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from appointments.models import AppointmentRequest
from reviews.models import Review
from .models import Notification


def _create_notification(recipient, actor, verb, target_obj):
    """
    Вспомогательная функция для создания уведомлений.
    Предотвращает дублирование кода.
    """
    if not recipient or recipient == actor:
        return  # Не создаём уведомление самому себе или без получателя

    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_ct=ContentType.objects.get_for_model(target_obj),
        target_id=target_obj.id
    )


@receiver(post_save, sender=AppointmentRequest)
def notify_doctor_new_request(sender, instance, created, **kwargs):
    """
    Уведомить врача о новой заявке на приём.
    """
    if created:
        _create_notification(
            recipient=instance.doctor,
            actor=instance.patient,
            verb='Новая заявка на приём',
            target_obj=instance
        )


@receiver(post_save, sender=AppointmentRequest)
def notify_patient_status_change(sender, instance, created, **kwargs):
    """
    Уведомить пациента об изменении статуса заявки.
    """
    if not created and instance.status in (
        AppointmentRequest.Status.ACCEPTED,
        AppointmentRequest.Status.REJECTED
    ):
        verb = (
            'Заявка принята'
            if instance.status == AppointmentRequest.Status.ACCEPTED
            else 'Заявка отклонена'
        )
        _create_notification(
            recipient=instance.patient,
            actor=instance.doctor,
            verb=verb,
            target_obj=instance
        )


@receiver(post_save, sender=Review)
def notify_doctor_new_review(sender, instance, created, **kwargs):
    """
    Уведомить врача о новом отзыве.
    """
    if created:
        _create_notification(
            recipient=instance.appointment.doctor,
            actor=instance.appointment.patient,
            verb='Новый отзыв',
            target_obj=instance
        )

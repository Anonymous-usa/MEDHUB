from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from appointments.models import AppointmentRequest
from reviews.models import Review
from .models import Notification

@receiver(post_save, sender=AppointmentRequest)
def notify_doctor_new_request(sender, instance, created, **kwargs):
    if created:
        # Уведомить врача о новой заявке
        Notification.objects.create(
            recipient=instance.doctor,
            actor=instance.patient,
            verb='Новая заявка на приём',
            target_ct=ContentType.objects.get_for_model(instance),
            target_id=instance.id
        )

@receiver(post_save, sender=AppointmentRequest)
def notify_patient_status_change(sender, instance, created, **kwargs):
    if not created and instance.status in (
        AppointmentRequest.Status.ACCEPTED,
        AppointmentRequest.Status.REJECTED
    ):
        # Уведомить пациента о смене статуса
        verb = 'Заявка принята' if instance.status == AppointmentRequest.Status.ACCEPTED else 'Заявка отклонена'
        Notification.objects.create(
            recipient=instance.patient,
            actor=instance.doctor,
            verb=verb,
            target_ct=ContentType.objects.get_for_model(instance),
            target_id=instance.id
        )

@receiver(post_save, sender=Review)
def notify_doctor_new_review(sender, instance, created, **kwargs):
    if created:
        # Уведомить врача о новом отзыве
        Notification.objects.create(
            recipient=instance.appointment.doctor,
            actor=instance.appointment.patient,
            verb='Новый отзыв',
            target_ct=ContentType.objects.get_for_model(instance),
            target_id=instance.id
        )

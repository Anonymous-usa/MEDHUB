from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings

User = settings.AUTH_USER_MODEL
class AppointmentRequest(models.Model):
    class Status(models.TextChoices):
        PENDING  = 'pending',  _('Ожидает')
        ACCEPTED = 'accepted', _('Принята')
        REJECTED = 'rejected', _('Отклонена')

    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='appointment_requests'
    )
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='incoming_requests'
    )
    note = models.TextField(blank=True, verbose_name=_('Комментарий пациента'))
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_('Статус заявки')
    )
    appointment_time = models.DateTimeField(null=True, blank=True, verbose_name=_('Время приёма'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активна'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создана'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Обновлена'))

    class Meta:
        verbose_name = _('Заявка на приём')
        verbose_name_plural = _('Заявки на приём')
        ordering = ('-created_at',)
        unique_together = ('patient', 'doctor')
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['doctor']),
            models.Index(fields=['patient']),
        ]

    def clean(self):
        if self.patient_id == self.doctor_id:
            raise ValidationError(_('Пациент и врач не могут быть одним и тем же пользователем'))
        if not hasattr(self.patient, 'user_type') or self.patient.user_type != self.patient.UserType.PATIENT:
            raise ValidationError(_('Создавать заявку может только пациент'))
        if not hasattr(self.doctor, 'user_type') or self.doctor.user_type != self.doctor.UserType.DOCTOR:
            raise ValidationError(_('Назначать приём можно только к врачу'))

    def __str__(self):
        return f"{self.patient} → {self.doctor} [{self.status}]"

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings

User = settings.AUTH_USER_MODEL


class AppointmentRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Ожидает')
        ACCEPTED = 'accepted', _('Принята')
        REJECTED = 'rejected', _('Отклонена')
        CANCELLED = 'cancelled', _('Отменена')  # 🔥 добавил для полноты логики

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointment_requests',
        verbose_name=_('Пациент')
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='incoming_requests',
        verbose_name=_('Врач')
    )
    note = models.TextField(
        blank=True,
        verbose_name=_('Комментарий пациента')
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('Статус заявки')
    )
    appointment_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Время приёма')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Активна')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Создана')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Обновлена')
    )

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
        """
        Валидация бизнес-логики:
        - Пациент и врач не могут совпадать
        - Пациент должен быть с ролью PATIENT
        - Врач должен быть с ролью DOCTOR
        """
        if self.patient_id == self.doctor_id:
            raise ValidationError(_('Пациент и врач не могут быть одним и тем же пользователем'))

        if not self.patient.is_patient():
            raise ValidationError(_('Создавать заявку может только пациент'))

        if not self.doctor.is_doctor():
            raise ValidationError(_('Назначать приём можно только к врачу'))

    def __str__(self):
        return f"{self.patient} → {self.doctor} [{self.get_status_display()}]"

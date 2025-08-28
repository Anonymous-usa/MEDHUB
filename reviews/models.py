# reviews/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from core.models import TimeStampedModel
from appointments.models import AppointmentRequest


User = settings.AUTH_USER_MODEL


class Review(TimeStampedModel):
    """
    Отзыв пациента о приёме.
    Привязан к конкретной заявке (AppointmentRequest) один к одному.
    """
    appointment = models.OneToOneField(
        AppointmentRequest,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name=_('Заявка')
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name=_('Оценка')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Комментарий')
    )

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rating']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.appointment.patient} → {self.appointment.doctor}: {self.rating}'

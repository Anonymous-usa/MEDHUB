from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from appointments.models import AppointmentRequest

User = settings.AUTH_USER_MODEL

class Review(models.Model):
    appointment = models.OneToOneField(
        AppointmentRequest,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name=_('Заявка')
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name=_('Оценка'),
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Комментарий')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')

    def __str__(self):
        return f'{self.appointment.patient} → {self.appointment.doctor}: {self.rating}'

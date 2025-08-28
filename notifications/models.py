# notification/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from core.models import TimeStampedModel

User = settings.AUTH_USER_MODEL


class Notification(TimeStampedModel):
    """
    Универсальные уведомления для пользователей.
    Могут ссылаться на любой объект (AppointmentRequest, Review, и т.д.)
    через generic foreign key.
    """
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('Получатель')
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actor_notifications',
        verbose_name=_('Инициатор')
    )
    verb = models.CharField(max_length=255, verbose_name=_('Действие'))

    # Generic link to any object (AppointmentRequest, Review, etc.)
    target_ct = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')

    is_read = models.BooleanField(default=False, verbose_name=_('Прочитано'))

    class Meta:
        verbose_name = _('Уведомление')
        verbose_name_plural = _('Уведомления')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient']),
            models.Index(fields=['is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"[{self.recipient}] {self.verb}"

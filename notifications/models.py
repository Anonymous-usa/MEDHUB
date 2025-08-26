from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    recipient     = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications',
        verbose_name=_('Получатель')
    )
    actor         = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='actor_notifications', verbose_name=_('Инициатор')
    )
    verb          = models.CharField(max_length=255, verbose_name=_('Действие'))
    # Generic link to any object (AppointmentRequest, Review, etc.)
    target_ct     = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    target_id     = models.PositiveIntegerField(null=True, blank=True)
    target        = GenericForeignKey('target_ct', 'target_id')
    is_read       = models.BooleanField(default=False, verbose_name=_('Прочитано'))
    created_at    = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата'))

    class Meta:
        verbose_name = _('Уведомление')
        verbose_name_plural = _('Уведомления')
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.recipient}] {self.verb}'

# message/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from core.models import TimeStampedModel


class Message(TimeStampedModel):
    """
    Сообщения между пользователями (пациентами, врачами, администраторами).
    """
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name=_("Отправитель")
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages",
        verbose_name=_("Получатель")
    )
    content = models.TextField(verbose_name=_("Текст сообщения"))
    is_read = models.BooleanField(default=False, verbose_name=_("Прочитано"))

    class Meta:
        verbose_name = _("Сообщение")
        verbose_name_plural = _("Сообщения")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["sender"]),
            models.Index(fields=["receiver"]),
            models.Index(fields=["is_read"]),
        ]

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({'прочитано' if self.is_read else 'новое'})"

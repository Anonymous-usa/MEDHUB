from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from core.models import TimeStampedModel


class Message(TimeStampedModel):
    """
    Сообщения между пользователями (пациентами, врачами, администраторами).
    """

    class MessageStatus(models.TextChoices):
        SENT = "sent", _("Отправлено")
        DELIVERED = "delivered", _("Доставлено")
        READ = "read", _("Прочитано")

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

    # Новый статус (более гибкий, чем просто is_read)
    status = models.CharField(
        max_length=20,
        choices=MessageStatus.choices,
        default=MessageStatus.SENT,
        verbose_name=_("Статус")
    )

    # Возможность прикреплять файлы (опционально)
    attachment = models.FileField(
        upload_to="messages/attachments/",
        blank=True,
        null=True,
        verbose_name=_("Вложение")
    )

    class Meta:
        verbose_name = _("Сообщение")
        verbose_name_plural = _("Сообщения")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["sender"]),
            models.Index(fields=["receiver"]),
            models.Index(fields=["is_read"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.get_status_display()})"

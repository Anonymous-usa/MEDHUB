# statistics/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models import TimeStampedModel


class StatisticRecord(TimeStampedModel):
    """
    Хранит агрегированные показатели (глобальные или привязанные к объекту)
    за определённый период.
    Пример:
    - Кол-во приёмов за день для конкретного врача
    - Средний рейтинг учреждения за месяц
    - Общее число новых пользователей в системе
    """
    metric = models.CharField(
        max_length=255,
        verbose_name=_("Название метрики")
    )
    value = models.FloatField(
        verbose_name=_("Значение")
    )

    # Период, к которому относится метрика
    period_start = models.DateField(verbose_name=_("Начало периода"))
    period_end = models.DateField(verbose_name=_("Конец периода"))

    # (опционально) Привязка к конкретному объекту: врач, учреждение и т.д.
    target_ct = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_ct", "target_id")

    class Meta:
        verbose_name = _("Статистический показатель")
        verbose_name_plural = _("Статистические показатели")
        indexes = [
            models.Index(fields=["metric", "period_start", "period_end"]),
            models.Index(fields=["target_ct", "target_id"]),
        ]
        unique_together = ("metric", "period_start", "period_end", "target_ct", "target_id")
        ordering = ["-period_start"]

    def __str__(self):
        scope = f" for {self.target}" if self.target else ""
        return f"{self.metric} ({self.period_start} → {self.period_end}){scope}: {self.value}"

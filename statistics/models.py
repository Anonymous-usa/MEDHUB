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
    Примеры:
    - Кол-во приёмов за день для конкретного врача
    - Средний рейтинг учреждения за месяц
    - Общее число новых пользователей в системе
    """

    class MetricType(models.TextChoices):
        APPOINTMENTS_COUNT = "appointments_count", _("Количество приёмов")
        AVG_RATING = "avg_rating", _("Средний рейтинг")
        NEW_USERS = "new_users", _("Новые пользователи")
        CUSTOM = "custom", _("Пользовательская метрика")

    metric = models.CharField(
        max_length=50,
        choices=MetricType.choices,
        verbose_name=_("Название метрики")
    )

    # Используем DecimalField для точности (например, средний рейтинг 4.37)
    value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
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
        return f"{self.get_metric_display()} ({self.period_start} → {self.period_end}){scope}: {self.value}"

    # 🔧 Удобный метод для выборки
    @classmethod
    def get_for_period(cls, metric, start, end, target=None):
        qs = cls.objects.filter(metric=metric, period_start=start, period_end=end)
        if target:
            qs = qs.filter(
                target_ct=ContentType.objects.get_for_model(target),
                target_id=target.id
            )
        return qs.first()

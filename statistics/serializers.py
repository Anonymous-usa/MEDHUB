from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class SystemOverviewStatsSerializer(serializers.Serializer):
    """
    Обзорные показатели по всей системе.
    """
    period_start = serializers.DateField(label=_("Начало периода"))
    period_end = serializers.DateField(label=_("Конец периода"))

    total_institutions = serializers.IntegerField(label=_("Всего учреждений"))
    total_hospitals = serializers.IntegerField(label=_("Всего больниц"))
    total_clinics = serializers.IntegerField(label=_("Всего клиник"))
    total_doctors = serializers.IntegerField(label=_("Всего врачей"))
    total_patients = serializers.IntegerField(label=_("Всего пациентов"))
    total_requests = serializers.IntegerField(label=_("Всего заявок"))
    accepted_requests = serializers.IntegerField(label=_("Принятые заявки"))
    rejected_requests = serializers.IntegerField(label=_("Отклонённые заявки"))


class InstitutionSpecificStatsSerializer(serializers.Serializer):
    """
    Показатели по конкретному учреждению.
    """
    period_start = serializers.DateField(label=_("Начало периода"))
    period_end = serializers.DateField(label=_("Конец периода"))

    institution_id = serializers.IntegerField(label=_("ID учреждения"))
    name = serializers.CharField(label=_("Название учреждения"))
    total_doctors = serializers.IntegerField(label=_("Всего врачей"))
    total_requests = serializers.IntegerField(label=_("Всего заявок"))
    accepted_requests = serializers.IntegerField(label=_("Принятые заявки"))
    rejected_requests = serializers.IntegerField(label=_("Отклонённые заявки"))
    avg_rating = serializers.DecimalField(
        max_digits=3, decimal_places=2,
        label=_("Средний рейтинг"),
        help_text=_("Средняя оценка врачей учреждения"),
        required=False
    )


class MetricSerializer(serializers.Serializer):
    """
    Универсальный сериализатор для произвольных метрик (например, для графиков).
    """
    metric = serializers.CharField(label=_("Метрика"))
    value = serializers.DecimalField(max_digits=12, decimal_places=2)
    period_start = serializers.DateField()
    period_end = serializers.DateField()

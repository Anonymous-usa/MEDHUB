from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class SystemOverviewStatsSerializer(serializers.Serializer):
    """
    Обзорные показатели по всей системе.
    """
    total_institutions = serializers.IntegerField(
        label=_("Всего учреждений"),
        help_text=_("Общее количество зарегистрированных учреждений")
    )
    total_hospitals = serializers.IntegerField(
        label=_("Всего больниц"),
        help_text=_("Количество учреждений типа 'больница'")
    )
    total_clinics = serializers.IntegerField(
        label=_("Всего клиник"),
        help_text=_("Количество учреждений типа 'клиника'")
    )
    total_doctors = serializers.IntegerField(
        label=_("Всего врачей"),
        help_text=_("Общее количество зарегистрированных врачей")
    )
    total_patients = serializers.IntegerField(
        label=_("Всего пациентов"),
        help_text=_("Общее количество зарегистрированных пациентов")
    )
    total_requests = serializers.IntegerField(
        label=_("Всего заявок"),
        help_text=_("Общее количество заявок на приём")
    )
    accepted_requests = serializers.IntegerField(
        label=_("Принятые заявки"),
        help_text=_("Количество заявок со статусом 'Принята'")
    )
    rejected_requests = serializers.IntegerField(
        label=_("Отклонённые заявки"),
        help_text=_("Количество заявок со статусом 'Отклонена'")
    )


class InstitutionSpecificStatsSerializer(serializers.Serializer):
    """
    Показатели по конкретному учреждению.
    """
    institution_id = serializers.IntegerField(
        label=_("ID учреждения"),
        help_text=_("Уникальный идентификатор учреждения")
    )
    name = serializers.CharField(
        label=_("Название учреждения"),
        help_text=_("Отображаемое название учреждения")
    )
    total_doctors = serializers.IntegerField(
        label=_("Всего врачей"),
        help_text=_("Количество врачей, связанных с учреждением")
    )
    total_requests = serializers.IntegerField(
        label=_("Всего заявок"),
        help_text=_("Общее количество заявок, связанных с учреждением")
    )
    accepted_requests = serializers.IntegerField(
        label=_("Принятые заявки"),
        help_text=_("Количество заявок, принятых врачами учреждения")
    )
    rejected_requests = serializers.IntegerField(
        label=_("Отклонённые заявки"),
        help_text=_("Количество заявок, отклонённых врачами учреждения")
    )

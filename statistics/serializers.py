# statistics/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class OverviewStatsSerializer(serializers.Serializer):
    """
    Обзорные показатели по всей системе.
    """
    total_institutions = serializers.IntegerField(label=_("Всего учреждений"))
    total_hospitals = serializers.IntegerField(label=_("Всего больниц"))
    total_clinics = serializers.IntegerField(label=_("Всего клиник"))
    total_doctors = serializers.IntegerField(label=_("Всего врачей"))
    total_patients = serializers.IntegerField(label=_("Всего пациентов"))
    total_requests = serializers.IntegerField(label=_("Всего заявок"))
    accepted_requests = serializers.IntegerField(label=_("Принятые заявки"))
    rejected_requests = serializers.IntegerField(label=_("Отклонённые заявки"))


class InstitutionStatsSerializer(serializers.Serializer):
    """
    Показатели по конкретному учреждению.
    """
    institution_id = serializers.IntegerField(label=_("ID учреждения"))
    name = serializers.CharField(label=_("Название учреждения"))
    total_doctors = serializers.IntegerField(label=_("Всего врачей"))
    total_requests = serializers.IntegerField(label=_("Всего заявок"))
    accepted_requests = serializers.IntegerField(label=_("Принятые заявки"))
    rejected_requests = serializers.IntegerField(label=_("Отклонённые заявки"))

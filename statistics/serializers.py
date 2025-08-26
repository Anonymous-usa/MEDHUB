from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class OverviewStatsSerializer(serializers.Serializer):
    total_institutions     = serializers.IntegerField()
    total_hospitals        = serializers.IntegerField()
    total_clinics          = serializers.IntegerField()
    total_doctors          = serializers.IntegerField()
    total_patients         = serializers.IntegerField()
    total_requests         = serializers.IntegerField()
    accepted_requests      = serializers.IntegerField()
    rejected_requests      = serializers.IntegerField()


class InstitutionStatsSerializer(serializers.Serializer):
    institution_id         = serializers.IntegerField()
    name                   = serializers.CharField()
    total_doctors          = serializers.IntegerField()
    total_requests         = serializers.IntegerField()
    accepted_requests      = serializers.IntegerField()
    rejected_requests      = serializers.IntegerField()

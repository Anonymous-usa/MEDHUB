# institutions/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Institution, Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)


class InstitutionAdminSerializer(serializers.ModelSerializer):
    """
    Для операций super_admin и institution_admin.
    """
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model  = Institution
        fields = (
            'id', 'name', 'slug', 'description',
            'institution_type', 'ownership_type',
            'region', 'address', 'phone', 'email',
            'latitude', 'longitude', 'logo',
            'is_top', 'is_active',
            'departments', 'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')


class InstitutionPublicSerializer(serializers.ModelSerializer):
    """
    Только для публичного списка и деталки.
    """
    logo_url    = serializers.SerializerMethodField()
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model  = Institution
        fields = (
            'id', 'name', 'slug', 'description',
            'institution_type', 'ownership_type',
            'region', 'address', 'phone', 'email',
            'latitude', 'longitude', 'logo_url',
            'is_top', 'departments'
        )

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        return None

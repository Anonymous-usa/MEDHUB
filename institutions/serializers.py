from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from .models import Institution, Department
from core.serializers import CitySerializer


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Сериализатор отделения учреждения.
    """
    class Meta:
        model = Department
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)


class InstitutionAdminSerializer(serializers.ModelSerializer):
    """
    Для операций super_admin и institution_admin.
    Полный набор данных + отделения (read-only).
    """
    departments = DepartmentSerializer(many=True, read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    region_name = serializers.CharField(source='city.region.name', read_only=True)

    class Meta:
        model = Institution
        fields = (
            'id', 'name', 'slug', 'description',
            'institution_type', 'ownership_type',
            'city', 'city_name', 'region_name',
            'address', 'phone', 'email',
            'latitude', 'longitude', 'logo',
            'is_top', 'is_active',
            'departments', 'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')


class InstitutionPublicSerializer(serializers.ModelSerializer):
    """
    Только для публичного списка и деталки.
    """
    @extend_schema_field(OpenApiTypes.STR)
    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        return None

    logo_url = serializers.SerializerMethodField()
    departments = DepartmentSerializer(many=True, read_only=True)
    city = CitySerializer(read_only=True)
    region_name = serializers.CharField(source='city.region.name', read_only=True)

    class Meta:
        model = Institution
        fields = (
            'id', 'name', 'slug', 'description',
            'institution_type', 'ownership_type',
            'city', 'region_name',
            'address', 'phone', 'email',
            'latitude', 'longitude', 'logo_url',
            'is_top', 'departments'
        )



class InstitutionRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = [
            'name', 'slug', 'institution_type', 'ownership_type',
            'region', 'city', 'address', 'phone', 'email',
            'description',  'is_active', 'is_top'
        ]

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import Institution, Department
from core.serializers import CitySerializer
from accounts.models import User

# 🔹 Отделения
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)

# 🔹 Админ сериализатор учреждения
class InstitutionAdminSerializer(serializers.ModelSerializer):
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

# 🔹 Публичный сериализатор учреждения
class InstitutionPublicSerializer(serializers.ModelSerializer):
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

# 🔹 Регистрация учреждения + администратора
class InstitutionWithAdminSerializer(serializers.Serializer):
    name = serializers.CharField()
    region = serializers.CharField()
    city = serializers.CharField()

    admin_first_name = serializers.CharField()
    admin_last_name = serializers.CharField()
    admin_email = serializers.EmailField()
    admin_phone = serializers.CharField()
    admin_date_of_birth = serializers.DateField()
    admin_password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        institution = Institution.objects.create(
            name=validated_data['name'],
            region=validated_data['region'],
            city=validated_data['city'],
        )

        User.objects.create_user(
            first_name=validated_data['admin_first_name'],
            last_name=validated_data['admin_last_name'],
            email=validated_data['admin_email'],
            phone_number=validated_data['admin_phone'],
            date_of_birth=validated_data['admin_date_of_birth'],
            password=validated_data['admin_password'],
            user_type=User.UserType.INSTITUTION_ADMIN,
            institution=institution,
            is_verified=True,
            is_active=True,
        )

        return institution


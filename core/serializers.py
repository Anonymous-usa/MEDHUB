from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import Region, City


class RegionSerializer(serializers.ModelSerializer):
    """
    Сериализатор региона с базовыми полями.
    """
    class Meta:
        model = Region
        fields = ('id', 'name', 'slug')


class CitySerializer(serializers.ModelSerializer):
    """
    Сериализатор города с вложенными данными региона.
    """
    region_name = serializers.SerializerMethodField()
    region_slug = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_region_name(self, obj):
        return obj.region.name if obj.region else None

    @extend_schema_field(OpenApiTypes.STR)
    def get_region_slug(self, obj):
        return obj.region.slug if obj.region else None

    class Meta:
        model = City
        fields = (
            'id',
            'name',
            'slug',
            'region',       # ID региона
            'region_name',  # Читаемое имя региона
            'region_slug',  # Slug региона
        )
        extra_kwargs = {
            'region': {'write_only': True}  # при создании передаём только id региона
        }

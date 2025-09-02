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
    Сериализатор города с вложенным регионом.
    """

    @extend_schema_field(OpenApiTypes.STR)
    def get_region_name(self):
        return self.region.name

    @extend_schema_field(OpenApiTypes.STR)
    def get_region_slug(self):
        return self.region.slug

    region_name = serializers.SerializerMethodField()
    region_slug = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ('id', 'name', 'slug', 'region', 'region_name', 'region_slug')

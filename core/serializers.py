from rest_framework import serializers
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
    region_name = serializers.CharField(source='region.name', read_only=True)
    region_slug = serializers.SlugField(source='region.slug', read_only=True)

    class Meta:
        model = City
        fields = ('id', 'name', 'slug', 'region', 'region_name', 'region_slug')

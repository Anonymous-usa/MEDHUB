from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Region, City
from .serializers import RegionSerializer, CitySerializer

class RegionListView(generics.ListAPIView):
    """
    Публичный список регионов.
    """
    queryset = Region.objects.filter(is_active=True)
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]


class CityListView(generics.ListAPIView):
    """
    Список городов в выбранном регионе.
    """
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        region_slug = self.kwargs.get('region_slug')
        return City.objects.filter(region__slug=region_slug, is_active=True)

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Region, City
from .serializers import RegionSerializer, CitySerializer

class RegionListView(generics.ListAPIView):
    """
    Публичный список активных регионов Таджикистана.
    """
    queryset = Region.objects.filter(is_active=True).order_by('name')
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]


class CityListView(generics.ListAPIView):
    """
    Список активных городов в выбранном регионе.
    """
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        region_slug = self.kwargs.get('region_slug')
        return City.objects.filter(
            region__slug=region_slug,
            is_active=True
        ).order_by('name')

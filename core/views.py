from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Region, City
from .serializers import RegionSerializer, CitySerializer

@extend_schema(
    responses={200: RegionSerializer},
    description="Публичный список активных регионов Таджикистана"
)
class RegionListView(generics.ListAPIView):
    queryset = Region.objects.filter(is_active=True).order_by('name')
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="region_slug",
            location=OpenApiParameter.PATH,
            required=True,
            type=str,
            description="Slug региона"
        )
    ],
    responses={200: CitySerializer},
    description="Список активных городов в выбранном регионе"
)
class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return City.objects.none()
        region_slug: str = self.kwargs.get('region_slug')
        return City.objects.filter(
            region__slug=region_slug,
            is_active=True
        ).order_by('name')

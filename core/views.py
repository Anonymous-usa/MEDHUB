from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Region, City
from .serializers import RegionSerializer, CitySerializer


@extend_schema(
    tags=["Core"],
    summary="Список регионов",
    description="Возвращает публичный список всех активных регионов Таджикистана.",
    responses={200: RegionSerializer(many=True)},
)
class RegionListView(generics.ListAPIView):
    """
    Публичный список всех активных регионов.
    """
    queryset = Region.objects.filter(is_active=True).order_by('name')
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]


@extend_schema(
    tags=["Core"],
    summary="Список городов региона",
    description="Возвращает список всех активных городов выбранного региона по его slug.",
    parameters=[
        OpenApiParameter(
            name="region_slug",
            location=OpenApiParameter.PATH,
            required=True,
            type=str,
            description="Slug региона (например: dushanbe, sughd)"
        )
    ],
    responses={200: CitySerializer(many=True)},
)
class CityListView(generics.ListAPIView):
    """
    Публичный список всех активных городов выбранного региона.
    """
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

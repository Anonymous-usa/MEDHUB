import logging
from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Institution, Department
from .serializers import InstitutionAdminSerializer, InstitutionPublicSerializer
from .permissions import IsSuperAdmin, IsInstitutionOwnerOrSuper

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        tags=["Institutions"],
        summary="Список учреждений",
        description="Возвращает публичный список всех активных учреждений.",
        responses={200: InstitutionPublicSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["Institutions"],
        summary="Информация об учреждении",
        description="Возвращает публичную информацию об учреждении по ID.",
        responses={200: InstitutionPublicSerializer},
    ),
    create=extend_schema(
        tags=["Institutions"],
        summary="Создать учреждение",
        description="Создаёт новое учреждение. Доступно только супер‑админу.",
        request=InstitutionAdminSerializer,
        responses={201: InstitutionAdminSerializer},
    ),
    update=extend_schema(
        tags=["Institutions"],
        summary="Обновить учреждение",
        description="Обновление данных учреждения. Доступно администратору учреждения или супер‑админу.",
        request=InstitutionAdminSerializer,
        responses={200: InstitutionAdminSerializer},
    ),
    partial_update=extend_schema(
        tags=["Institutions"],
        summary="Частичное обновление учреждения",
        description="Частичное обновление данных учреждения. Доступно администратору учреждения или супер‑админу.",
        request=InstitutionAdminSerializer,
        responses={200: InstitutionAdminSerializer},
    ),
    destroy=extend_schema(
        tags=["Institutions"],
        summary="Удалить учреждение",
        description="Удаление учреждения. Доступно только супер‑админу.",
        responses={204: None},
    )
)
class InstitutionViewSet(viewsets.ModelViewSet):
    """
    API для управления учреждениями.
    """
    queryset = Institution.objects.select_related('city', 'city__region').prefetch_related('departments')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['institution_type', 'ownership_type', 'city', 'is_top', 'is_active']
    search_fields = ['name', 'address', 'city__name', 'city__region__name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated(), IsSuperAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsInstitutionOwnerOrSuper()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsSuperAdmin()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return InstitutionPublicSerializer
        return InstitutionAdminSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"Учреждение создано: {instance.name} ({instance.slug})")

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(f"Учреждение обновлено: {instance.name} ({instance.slug})")

    def perform_destroy(self, instance):
        logger.warning(f"Учреждение удалено: {instance.name} ({instance.slug})")
        instance.delete()

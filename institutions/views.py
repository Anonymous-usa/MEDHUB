from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Institution
from .serializers import InstitutionAdminSerializer, InstitutionPublicSerializer
from .permissions import IsSuperAdmin, IsInstitutionOwnerOrSuper

import logging
logger = logging.getLogger(__name__)

@extend_schema_view(
    list=extend_schema(
        responses={200: InstitutionPublicSerializer},
        description="Публичный список учреждений"
    ),
    retrieve=extend_schema(
        responses={200: InstitutionPublicSerializer},
        description="Публичная информация об учреждении"
    ),
    create=extend_schema(
        request=InstitutionAdminSerializer,
        responses={201: InstitutionAdminSerializer},
        description="Создание учреждения (только супер-админ)"
    ),
    update=extend_schema(
        request=InstitutionAdminSerializer,
        responses={200: InstitutionAdminSerializer},
        description="Обновление учреждения (админ или супер-админ)"
    ),
    partial_update=extend_schema(
        request=InstitutionAdminSerializer,
        responses={200: InstitutionAdminSerializer},
        description="Частичное обновление учреждения"
    ),
    destroy=extend_schema(
        responses={204: None},
        description="Удаление учреждения (только супер-админ)"
    )
)
class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.select_related(
        'city', 'city__region'
    ).prefetch_related('departments')
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

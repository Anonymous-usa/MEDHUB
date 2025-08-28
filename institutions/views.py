# institutions/views.py
import logging
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Institution
from .serializers import (
    InstitutionAdminSerializer,
    InstitutionPublicSerializer
)
from .permissions import IsSuperAdmin, IsInstitutionOwnerOrSuper

logger = logging.getLogger(__name__)


class InstitutionViewSet(viewsets.ModelViewSet):
    """
    create:              супер-админ
    list/retrieve:       публично (AllowAny)
    update/partial_update: админ своего учреждения или супер-админ
    destroy:             только супер-админ
    """
    queryset = Institution.objects.select_related(
        'city', 'city__region'
    ).prefetch_related(
        'departments'
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['institution_type', 'ownership_type', 'city', 'is_top', 'is_active']
    search_fields = ['name', 'address', 'city__name', 'city__region__name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            perms = [AllowAny]
        elif self.action == 'create':
            perms = [IsAuthenticated, IsSuperAdmin]
        elif self.action in ['update', 'partial_update']:
            perms = [IsAuthenticated, IsInstitutionOwnerOrSuper]
        elif self.action == 'destroy':
            perms = [IsAuthenticated, IsSuperAdmin]
        else:
            perms = [IsAuthenticated]
        return [p() for p in perms]

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

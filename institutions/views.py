# institutions/views.py
from rest_framework import viewsets, generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Institution
from .serializers import (
    InstitutionAdminSerializer,
    InstitutionPublicSerializer
)
from .permissions import IsSuperAdmin, IsInstitutionOwnerOrSuper

class InstitutionViewSet(viewsets.ModelViewSet):
    """
    create:        супер-админ
    list/retrieve: публично (AllowAny)
    update/partial_update: админ своего учреждения или супер-админ
    destroy:       только супер-админ
    """
    queryset = Institution.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['institution_type', 'ownership_type', 'region', 'is_top']
    search_fields = ['name', 'address']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            perm = [AllowAny]
        elif self.action == 'create':
            perm = [IsAuthenticated, IsSuperAdmin]
        elif self.action in ['update', 'partial_update']:
            perm = [IsAuthenticated, IsInstitutionOwnerOrSuper]
        elif self.action == 'destroy':
            perm = [IsAuthenticated, IsSuperAdmin]
        else:
            perm = [IsAuthenticated]
        return [p() for p in perm]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return InstitutionPublicSerializer
        return InstitutionAdminSerializer

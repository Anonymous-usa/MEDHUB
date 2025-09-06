import logging
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Institution
from .serializers import (
    InstitutionAdminSerializer,
    InstitutionPublicSerializer,
    InstitutionWithAdminSerializer
)
from accounts.permissions import IsSuperAdmin, IsInstitutionOwnerOrSuper

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


@extend_schema(
    request=InstitutionWithAdminSerializer,
    responses={201: InstitutionWithAdminSerializer},
    description="Регистрация учреждения и администратора (только SuperUser)"
)
class InstitutionRegistrationView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request):
        serializer = InstitutionWithAdminSerializer(data=request.data)
        if serializer.is_valid():
            institution = serializer.save()
            return Response({"detail": "Учреждение и администратор успешно зарегистрированы"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Department
from .serializers import DepartmentSerializer
from accounts.models import User

@extend_schema_view(
    list=extend_schema(description="Список отделений"),
    retrieve=extend_schema(description="Детали отделения"),
    create=extend_schema(description="Создание отделения"),
    update=extend_schema(description="Обновление отделения"),
    partial_update=extend_schema(description="Частичное обновление отделения"),
    destroy=extend_schema(description="Удаление отделения"),
)
class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return Department.objects.select_related('institution')
        elif user.is_institution_admin():
            return Department.objects.filter(institution=user.institution)
        return Department.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_institution_admin():
            serializer.save(institution=user.institution)
        elif user.is_super_admin():
            serializer.save()

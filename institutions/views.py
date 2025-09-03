import logging
from rest_framework import viewsets, filters, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Institution
from .serializers import InstitutionAdminSerializer, InstitutionPublicSerializer, InstitutionRegistrationSerializer
from .permissions import IsSuperAdmin, IsInstitutionOwnerOrSuper

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


class IsSuperAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_authenticated and
            (request.user.is_superuser or request.user.is_super_admin())
        )


@extend_schema(
    request=InstitutionRegistrationSerializer,
    responses={201: InstitutionRegistrationSerializer},
    description="Регистрация нового медицинского учреждения"
)
class InstitutionRegistrationView(APIView):
    permission_classes = [IsSuperAdminOrSuperUser]

    def post(self, request):
        serializer = InstitutionRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            institution = serializer.save()
            logger.info(f"Institution registered: {institution.name}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Institution registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Institution
from .forms import InstitutionForm  

class InstitutionFormView(UserPassesTestMixin, CreateView):
    model = Institution
    form_class = InstitutionForm
    template_name = 'admim_custom/institutionregister.html'
    success_url = '/dashboard/'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_super_admin()

from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

class InstitutionEditView(UserPassesTestMixin, UpdateView):
    model = Institution
    form_class = InstitutionForm
    template_name = 'admim_custom/institution_edit.html'
    success_url = reverse_lazy('admim_custom:institutions')  

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_super_admin()
    


class InstitutionDeleteView(UserPassesTestMixin, DeleteView):
    model = Institution
    template_name = 'admim_custom/institution_delete.html'
    success_url = reverse_lazy('admim_custom:institutions')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_super_admin()

from django.views.generic.edit import CreateView
from .models import Department
from .forms import DepartmentForm

class DepartmentCreateView(UserPassesTestMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'admim_custom/department_create.html'
    success_url = '/institutions/'  # или куда тебе нужно

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_super_admin()

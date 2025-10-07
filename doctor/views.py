# doctor/views.py
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_spectacular.utils import extend_schema
from accounts.models import User
from .serializers import DoctorPublicSerializer
from .filters import DoctorFilter
from .permissions import CanDeleteDoctor

@extend_schema(
    tags=["Doctors"],
    summary="Список всех врачей",
    description="Публичный список активных врачей с пагинацией и поиском.",
    responses={200: DoctorPublicSerializer(many=True)},
)
class DoctorListView(ListAPIView):
    queryset = User.objects.filter(user_type="doctor", is_active=True)
    serializer_class = DoctorPublicSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DoctorFilter
    search_fields = ['email', 'specialization']

@extend_schema(
    tags=["Doctors"],
    summary="Удалить врача",
    description="Удаляет врача по ID. Доступно только супер‑админу и администратору учреждения.",
    responses={204: None}
)
class DoctorDeleteView(DestroyAPIView):
    queryset = User.objects.filter(user_type="doctor")
    permission_classes = [IsAuthenticated, CanDeleteDoctor]
    lookup_field = "pk"

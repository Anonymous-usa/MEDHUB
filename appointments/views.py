import logging
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import AppointmentRequest
from .serializers import (
    AppointmentRequestCreateSerializer,
    AppointmentRequestDetailSerializer,
    AppointmentStatusUpdateSerializer,
    AppointmentSuccessSerializer,
    AppointmentErrorSerializer
)
from .permissions import IsPatient, IsDoctor, IsOwnerOrDoctor, IsSuperAdmin

logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        tags=["Appointments"],
        summary="Список заявок пациента",
        description="Возвращает список активных заявок текущего пациента.",
        responses={200: AppointmentRequestDetailSerializer(many=True)},
    ),
    post=extend_schema(
        tags=["Appointments"],
        summary="Создать заявку на приём",
        description="Пациент создаёт новую заявку на приём к врачу.",
        request=AppointmentRequestCreateSerializer,
        responses={201: AppointmentSuccessSerializer, 400: AppointmentErrorSerializer},
    )
)
class PatientAppointmentListCreateView(generics.ListCreateAPIView):
    """
    Пациент: просмотр и создание своих заявок.
    """
    serializer_class = AppointmentRequestCreateSerializer
    permission_classes = [IsAuthenticated, IsPatient]
    throttle_classes = [AnonRateThrottle]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return AppointmentRequest.objects.none()
        return AppointmentRequest.objects.filter(
            patient=self.request.user,
            is_active=True
        ).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = AppointmentRequestDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            f"Пациент {self.request.user.phone_number} создал заявку к врачу {instance.doctor.phone_number}"
        )


@extend_schema(
    tags=["Appointments"],
    summary="Список заявок врача",
    description="Возвращает список входящих заявок для текущего врача (только ожидающие).",
    responses={200: AppointmentRequestDetailSerializer(many=True)},
)
class DoctorAppointmentListView(generics.ListAPIView):
    """
    Врач: просмотр входящих заявок (только ожидающих).
    """
    serializer_class = AppointmentRequestDetailSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return AppointmentRequest.objects.none()
        return AppointmentRequest.objects.filter(
            doctor=self.request.user,
            is_active=True,
            status=AppointmentRequest.Status.PENDING
        ).order_by('-created_at')


@extend_schema(
    tags=["Appointments"],
    summary="Обновление статуса заявки",
    description="Врач может принять или отклонить заявку. "
                "Супер‑админ имеет право обновить любую заявку.",
    request=AppointmentStatusUpdateSerializer,
    responses={200: AppointmentRequestDetailSerializer, 400: AppointmentErrorSerializer},
)
class AppointmentStatusUpdateView(generics.UpdateAPIView):
    """
    Врач: может принять или отклонить заявку.
    Супер-админ: имеет право обновить любую заявку.
    """
    serializer_class = AppointmentStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrDoctor | IsSuperAdmin]
    queryset = AppointmentRequest.objects.filter(is_active=True)
    lookup_url_kwarg = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            f"Пользователь {self.request.user.phone_number} обновил заявку {instance.id} → статус: {instance.status}"
        )

        if instance.status == AppointmentRequest.Status.ACCEPTED:
            AppointmentRequest.objects.filter(
                doctor=instance.doctor,
                status=AppointmentRequest.Status.PENDING
            ).exclude(id=instance.id).update(status=AppointmentRequest.Status.REJECTED)

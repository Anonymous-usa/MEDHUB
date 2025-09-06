from django.apps import apps
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .serializers import SystemOverviewStatsSerializer, InstitutionSpecificStatsSerializer
from .permissions import IsSuperAdmin, IsInstitutionOwnerOrSuper
from institutions.models import Institution

User = apps.get_model(*settings.AUTH_USER_MODEL.split('.')) if isinstance(settings.AUTH_USER_MODEL, str) else settings.AUTH_USER_MODEL
Appointment = apps.get_model('appointments', 'AppointmentRequest')


@extend_schema(
    responses={200: SystemOverviewStatsSerializer},
    description="Общая статистика по системе (только для супер-админа)"
)
class OverviewStatsView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        data = {
            'total_institutions': Institution.objects.count(),
            'total_hospitals': Institution.objects.filter(institution_type='hospital').count(),
            'total_clinics': Institution.objects.filter(institution_type='clinic').count(),
            'total_doctors': User.objects.filter(user_type='doctor').count(),
            'total_patients': User.objects.filter(user_type='patient').count(),
            'total_requests': Appointment.objects.count(),
            'accepted_requests': Appointment.objects.filter(status=Appointment.Status.ACCEPTED).count(),
            'rejected_requests': Appointment.objects.filter(status=Appointment.Status.REJECTED).count(),
        }
        serializer = SystemOverviewStatsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="pk",
            location=OpenApiParameter.PATH,
            required=True,
            type=int,
            description="ID учреждения"
        )
    ],
    responses={200: InstitutionSpecificStatsSerializer},
    description="Статистика по конкретному учреждению (для супер-админа и админа учреждения)"
)
class InstitutionStatsView(APIView):
    permission_classes = [IsInstitutionOwnerOrSuper]

    def get(self, request, pk: int):
        institution = get_object_or_404(Institution, pk=pk)
        qs = Appointment.objects.filter(doctor__institution_id=institution.id)

        data = {
            'institution_id': institution.id,
            'name': institution.name,
            'total_doctors': institution.staff.filter(user_type='doctor').count(),
            'total_requests': qs.count(),
            'accepted_requests': qs.filter(status=Appointment.Status.ACCEPTED).count(),
            'rejected_requests': qs.filter(status=Appointment.Status.REJECTED).count(),
        }
        serializer = InstitutionSpecificStatsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)



# for admin-panel

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from appointments.models import AppointmentRequest
from institutions.models import Institution
from reviews.models import Review

from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=["Admin Dashboard"],
    description="Статистика для админ-панели (учреждения, заявки, врачи, отзывы)",
    responses={200: dict}
)

class AdminDashboardStatsView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_super_admin() and not user.is_institution_admin():
            return Response({"detail": "Нет доступа"}, status=403)

        stats = {
            "appointments_total": AppointmentRequest.objects.count(),
            "appointments_accepted": AppointmentRequest.objects.filter(status="accepted").count(),
            "appointments_pending": AppointmentRequest.objects.filter(status="pending").count(),
            "appointments_rejected": AppointmentRequest.objects.filter(status="rejected").count(),
            "institutions_total": Institution.objects.count(),
            "doctors_total": User.objects.filter(user_type=User.UserType.DOCTOR).count(),
            "reviews_total": Review.objects.count(),
        }
        return Response(stats)
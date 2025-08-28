# statistics/views.py
from django.apps import apps
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import OverviewStatsSerializer, InstitutionStatsSerializer
from .permissions import IsSuperAdmin, IsInstitutionOwnerOrSuper
from institutions.models import Institution

User = apps.get_model(*settings.AUTH_USER_MODEL.split('.')) if isinstance(settings.AUTH_USER_MODEL, str) else settings.AUTH_USER_MODEL
Appointment = apps.get_model('appointments', 'AppointmentRequest')


class OverviewStatsView(APIView):
    """
    GET /api/v1/stats/overview/
    Только для супер-админа: общая статистика по системе.
    """
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
        serializer = OverviewStatsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InstitutionStatsView(APIView):
    """
    GET /api/v1/stats/institution/<int:pk>/
    Для супер-админа и админа своего учреждения.
    """
    permission_classes = [IsInstitutionOwnerOrSuper]

    def get(self, request, pk):
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
        serializer = InstitutionStatsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

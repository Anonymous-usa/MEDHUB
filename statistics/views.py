from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from .serializers import OverviewStatsSerializer, InstitutionStatsSerializer
from .permissions import IsSuperAdmin, IsInstitutionOwnerOrSuper
from institutions.models import Institution
from django.conf import settings
User = settings.AUTH_USER_MODEL if isinstance(settings.AUTH_USER_MODEL, str) else settings.AUTH_USER_MODEL

class OverviewStatsView(APIView):
    """
    /api/v1/stats/overview/
    Только для супер-админа: общая статистика по системе.
    """
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        from django.apps import apps
        Appointment = apps.get_model('appointments', 'AppointmentRequest')

        total_institutions  = Institution.objects.count()
        total_hospitals     = Institution.objects.filter(institution_type='hospital').count()
        total_clinics       = Institution.objects.filter(institution_type='clinic').count()
        total_doctors       = User.objects.filter(user_type='doctor').count()
        total_patients      = User.objects.filter(user_type='patient').count()
        total_requests      = Appointment.objects.count()
        accepted_requests   = Appointment.objects.filter(status=Appointment.Status.ACCEPTED).count()
        rejected_requests   = Appointment.objects.filter(status=Appointment.Status.REJECTED).count()

        data = {
            'total_institutions': total_institutions,
            'total_hospitals': total_hospitals,
            'total_clinics': total_clinics,
            'total_doctors': total_doctors,
            'total_patients': total_patients,
            'total_requests': total_requests,
            'accepted_requests': accepted_requests,
            'rejected_requests': rejected_requests,
        }
        serializer = OverviewStatsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InstitutionStatsView(APIView):
    """
    /api/v1/stats/institution/<int:pk>/
    Для супер-админа и админа своего учреждения: статистика по конкретному учреждению.
    """
    permission_classes = [IsInstitutionOwnerOrSuper]

    def get_object(self):
        return Institution.objects.get(pk=self.kwargs['pk'])

    def get(self, request, pk):
        from django.apps import apps
        Appointment = apps.get_model('appointments', 'AppointmentRequest')

        institution = self.get_object()
        # общее число врачей в учреждении
        total_doctors = institution.staff.filter(user_type='doctor').count()
        # заявки к врачам этого учреждения
        qs = Appointment.objects.filter(doctor__institution_id=institution.id)
        total_requests    = qs.count()
        accepted_requests = qs.filter(status=Appointment.Status.ACCEPTED).count()
        rejected_requests = qs.filter(status=Appointment.Status.REJECTED).count()

        data = {
            'institution_id': institution.id,
            'name': institution.name,
            'total_doctors': total_doctors,
            'total_requests': total_requests,
            'accepted_requests': accepted_requests,
            'rejected_requests': rejected_requests,
        }
        serializer = InstitutionStatsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

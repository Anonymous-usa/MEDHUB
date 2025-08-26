from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AppointmentRequest
from .serializers import (
    AppointmentRequestCreateSerializer,
    AppointmentRequestDetailSerializer,
    AppointmentStatusUpdateSerializer
)
from .permissions import IsPatient, IsDoctor, IsOwnerOrDoctor

# Пациент: создать и просмотреть свои заявки
class PatientAppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentRequestCreateSerializer
    permission_classes = [IsPatient]
    
    def get_queryset(self):
        return AppointmentRequest.objects.filter(patient=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = AppointmentRequestDetailSerializer(queryset, many=True)
        return Response(serializer.data)

# Врач: список входящих заявок и деталка
class DoctorAppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentRequestDetailSerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        return AppointmentRequest.objects.filter(doctor=self.request.user)

# Врач: принять или отклонить заявку
class AppointmentStatusUpdateView(generics.UpdateAPIView):
    serializer_class = AppointmentStatusUpdateSerializer
    permission_classes = [IsDoctor, IsOwnerOrDoctor]
    queryset = AppointmentRequest.objects.all()
    lookup_url_kwarg = 'pk'

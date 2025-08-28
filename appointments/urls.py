from django.urls import path
from .views import (
    PatientAppointmentListCreateView,
    DoctorAppointmentListView,
    AppointmentStatusUpdateView
)

app_name = 'appointments'

urlpatterns = [
    # Пациент: создание и просмотр своих заявок
    path('v1/patient/appointments/', 
        PatientAppointmentListCreateView.as_view(), 
        name='patient-appointments'
    ),

    # Врач: просмотр входящих заявок
    path('v1/doctor/appointments/', 
        DoctorAppointmentListView.as_view(), 
        name='doctor-appointments'
    ),

    # Врач: обновление статуса заявки
    path('v1/doctor/appointments/<int:pk>/status/', 
        AppointmentStatusUpdateView.as_view(), 
        name='appointment-status-update'
    ),
]

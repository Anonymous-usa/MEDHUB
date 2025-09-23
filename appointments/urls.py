from django.urls import path
from .views import (
    PatientAppointmentListCreateView,
    DoctorAppointmentListView,
    AppointmentStatusUpdateView
)

app_name = 'appointments'

urlpatterns = [
    path('v1/patient/appointments/', 
        PatientAppointmentListCreateView.as_view(), 
        name='patient-appointments'
    ),
    path('v1/doctor/appointments/', 
        DoctorAppointmentListView.as_view(), 
        name='doctor-appointments'
    ),
    path('v1/doctor/appointments/<int:pk>/status/', 
        AppointmentStatusUpdateView.as_view(), 
        name='appointment-status-update'
    ),
]

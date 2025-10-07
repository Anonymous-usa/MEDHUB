# doctor/urls.py
from django.urls import path
from .views import DoctorListView, DoctorDeleteView

urlpatterns = [
    path("", DoctorListView.as_view(), name="doctor-list"),
    path("<int:pk>/", DoctorDeleteView.as_view(), name="doctor-delete"),
]

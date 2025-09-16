from django.urls import path
from .views import PatientReviewListCreateView, DoctorReviewListView

app_name = "reviews"

urlpatterns = [
    path("v1/patient/reviews/", PatientReviewListCreateView.as_view(), name="patient-reviews"),
    path("v1/doctors/<int:doctor_id>/reviews/", DoctorReviewListView.as_view(), name="doctor-reviews"),
]

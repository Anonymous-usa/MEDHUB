from django.urls import path
from .views import PatientRegistrationView, LoginView, UserProfileView, LogoutView

app_name = 'accounts_api'

urlpatterns = [
    path('v1/register/patient/', PatientRegistrationView.as_view(), name='patient-register'),
    path('v1/login/',           LoginView.as_view(),              name='login'),
    path('v1/profile/',         UserProfileView.as_view(),        name='profile'),
    path('v1/logout/',          LogoutView.as_view(),             name='logout'),
]

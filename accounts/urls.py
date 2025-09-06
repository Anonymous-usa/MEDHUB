# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import (
#     PatientRegistrationView,
#     LoginView,
#     UserProfileView,
#     LogoutView,
#     DoctorViewSet
# )

# app_name = 'accounts'

# router = DefaultRouter()
# router.register(r'doctors', DoctorViewSet, basename='doctor')

# urlpatterns = [
#     # API endpoints
#     path('v1/register/patient/', PatientRegistrationView.as_view(), name='patient-register'),
#     path('v1/login/',           LoginView.as_view(),              name='login'),
#     path('v1/profile/',         UserProfileView.as_view(),        name='user-profile'),
#     path('v1/logout/',          LogoutView.as_view(),             name='logout'),

#     # Doctor management
#     path('v1/', include(router.urls)),
# ]


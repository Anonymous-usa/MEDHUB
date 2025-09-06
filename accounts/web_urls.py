from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet

app_name = 'accounts_web'

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')

urlpatterns = [
    path('v1/', include(router.urls)),
]

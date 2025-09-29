from django.urls import path, include
from rest_framework.routers import DefaultRouter
from institutions.views import InstitutionViewSet, InstitutionRegistrationView

app_name = 'institutions'

router = DefaultRouter()
router.register(r'institutions', InstitutionViewSet, basename='institution')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/institutions/register/', InstitutionRegistrationView.as_view(), name='institution-register-api'),
]

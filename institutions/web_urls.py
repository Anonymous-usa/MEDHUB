from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstitutionViewSet, DepartmentViewSet, InstitutionRegistrationView

app_name = 'institutions_web'

router = DefaultRouter()
router.register(r'institutions', InstitutionViewSet, basename='institution')
router.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/institutions/register/', InstitutionRegistrationView.as_view(), name='institution-register'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from institutions.views import InstitutionViewSet

app_name = 'institutions'

router = DefaultRouter()
router.register(r'institutions', InstitutionViewSet, basename='institution')

urlpatterns = [
    path('v1/', include(router.urls)),
]

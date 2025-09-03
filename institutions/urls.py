from django.urls import path, include
from rest_framework.routers import DefaultRouter
from institutions.views import (
    InstitutionViewSet,
    InstitutionRegistrationView,
    InstitutionFormView, 
    InstitutionEditView, 
    InstitutionDeleteView,
    DepartmentCreateView
)

app_name = 'institutions'

router = DefaultRouter()
router.register(r'institutions', InstitutionViewSet, basename='institution')

urlpatterns = [
    # API endpoints
    path('v1/', include(router.urls)),
    path('api/register/', InstitutionRegistrationView.as_view(), name='institution-register-api'),

    # HTML форма регистрации учреждения
    path('register/', InstitutionFormView.as_view(), name='institution-register'),
    path('<int:pk>/edit/', InstitutionEditView.as_view(), name='institution-edit'),
    path('<int:pk>/delete/', InstitutionDeleteView.as_view(), name='institution-delete'),
    path('departments/create/', DepartmentCreateView.as_view(), name='department-create'),
]


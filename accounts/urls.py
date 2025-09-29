from django.urls import path
from .views import LoginView, RegisterView, ProfileView

app_name = 'accounts'

urlpatterns = [
    path('v1/auth/login/', LoginView.as_view(), name='login'),       # 🔑 Логин
    path('v1/auth/register/', RegisterView.as_view(), name='register'),  # 🆕 Регистрация
    path('v1/auth/me/', ProfileView.as_view(), name='me'),           # 👤 Профиль
]

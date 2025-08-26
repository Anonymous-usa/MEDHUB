# server/urls.py

from django.contrib import admin
from django.urls import path, include

# JWT-токен для обновления
from rest_framework_simplejwt.views import TokenRefreshView

# drf-spectacular
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),

    # Основные модули API
    path('api/', include('accounts.urls',      namespace='accounts')),
    path('api/', include('appointments.urls',  namespace='appointments')),
    path('api/', include('institutions.urls',  namespace='institutions')),
    path('api/', include('core.urls',          namespace='core')),
    path('api/', include('reviews.urls',       namespace='reviews')),
    path('api/', include('statistics.urls',    namespace='statistics')),
    path('api/', include('notifications.urls', namespace='notifications')),

    # Обновление JWT-токена
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # OpenAPI-схема в формате JSON/YAML
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI для интерактивной документации
    path(
        'api/docs/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),

    # Redoc UI альтернативная документация
    path(
        'api/docs/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]

# server/urls.py
from django.contrib import admin
from django.urls import path, include

# JWT refresh endpoint
from rest_framework_simplejwt.views import TokenRefreshView

# drf-spectacular views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from admim_custom import urls as admin_custom_urls

urlpatterns = [
    # 🛠 Админка Django
    path("admin/", admin.site.urls),
    # Админка Django
    path('admin/', admin.site.urls),
    path('admin/', include(admin_custom_urls)),  

    # 📦 Основные модули API (v1)
    path("api/", include("accounts.urls",      namespace="accounts")),
    path("api/", include("appointments.urls",  namespace="appointments")),
    path("api/", include("institutions.urls",  namespace="institutions")),
    path("api/", include("core.urls",          namespace="core")),
    path("api/", include("reviews.urls",       namespace="reviews")),
    path("api/", include("statistics.urls",    namespace="statistics")),
    path("api/", include("notifications.urls", namespace="notifications")),
    # If you add chat/WS routes, they would go here

    # 🔑 JWT — обновление access токена
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 📜 OpenAPI schema (JSON/YAML)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # 🖥 Swagger UI
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui"
    ),

    # 📘 ReDoc UI
    path(
        "api/docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc"
    ),
]

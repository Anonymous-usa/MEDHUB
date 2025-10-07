from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.contrib import admin

urlpatterns = [
    # 🛠 Кастомная админ-панель
    path("admin/", admin.site.urls),

    # 📦 Основные модули API (v1)
    path("api/v1/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("api/v1/", include(("appointments.urls", "appointments"), namespace="appointments")),
    
    path("api/v1/", include(("core.urls", "core"), namespace="core")),
    path("api/v1/", include(("reviews.urls", "reviews"), namespace="reviews")),
    path("api/v1/", include(("statistics.urls", "statistics"), namespace="statistics")),
    path("api/v1/", include(("notifications.urls", "notifications"), namespace="notifications")),
    path("api/v1/", include(("message.urls", "message"), namespace="message")),
    path("api/v1/doctors/", include("doctor.urls")),


    # 🔑 JWT — обновление access токена
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 📜 OpenAPI schema (JSON/YAML)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # 🖥 Swagger UI
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # 📘 ReDoc UI
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # 🌐 HTML-интерфейс учреждений (отдельный от API)
    path("institutions/", include(("institutions.urls", "institutions"), namespace="institutions-html")),
]

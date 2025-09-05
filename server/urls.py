from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# Кастомная админка MEDHUB.TJ
from admim_custom.admin_site import admin_site
from admim_custom import urls as admin_custom_urls

urlpatterns = [
    # 🛠 Кастомная админ-панель
    path("admin/", admin_site.urls),  # заменяет стандартную админку
    path("admin-panel/", include(admin_custom_urls, namespace="admim_custom")),

    # 📦 Основные модули API (v1)
    path("api/", include("accounts.urls",      namespace="accounts")),
    path("api/", include("appointments.urls",  namespace="appointments")),
    path("api/", include("institutions.urls",  namespace="institutions")),
    path("api/", include("core.urls",          namespace="core")),
    path("api/", include("reviews.urls",       namespace="reviews")),
    path("api/", include("statistics.urls",    namespace="statistics")),
    path("api/", include("notifications.urls", namespace="notifications")),
    path("api/", include("message.urls", namespace="message")),


    # 🔑 JWT — обновление access токена
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 📜 OpenAPI schema (JSON/YAML)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # 🖥 Swagger UI
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # 📘 ReDoc UI
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    
    # HTML-интерфейс учреждений
    path("institutions/", include("institutions.urls", namespace="institutions_admin")),

]

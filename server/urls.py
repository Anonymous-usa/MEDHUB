# from django.urls import path, include
# from rest_framework_simplejwt.views import TokenRefreshView
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularSwaggerView,
#     SpectacularRedocView,
# )

# # Кастомная админка MEDHUB.TJ
# from admim_custom.admin_site import admin_site
# from admim_custom import urls as admin_custom_urls

# urlpatterns = [
#     # 🛠 Кастомная админ-панель
#     path("admin/", admin_site.urls),  # заменяет стандартную админку
#     path("admin-panel/", include(admin_custom_urls, namespace="admim_custom")),

#     # 📦 Основные модули API (v1)
#     path("api/", include("accounts.urls",      namespace="accounts")),
#     path("api/", include("appointments.urls",  namespace="appointments")),
#     path("api/", include("institutions.urls",  namespace="institutions")),
#     path("api/", include("core.urls",          namespace="core")),
#     path("api/", include("reviews.urls",       namespace="reviews")),
#     path("api/", include("statistics.urls",    namespace="statistics")),
#     path("api/", include("notifications.urls", namespace="notifications")),
#     path("api/", include("message.urls", namespace="message")),


#     # 🔑 JWT — обновление access токена
#     path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

#     # 📜 OpenAPI schema (JSON/YAML)
#     path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

#     # 🖥 Swagger UI
#     path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

#     # 📘 ReDoc UI
#     path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    
#     # HTML-интерфейс учреждений
#     path("institutions/", include("institutions.urls", namespace="institutions_admin")),

# ]

from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # API
    path('api/schema/', SpectacularAPIView.as_view(urlconf='server.urls'), name='api-schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-swagger'),
    # path('api/', include('server.api_urls')),


    # WEB (admin)
    path('web/schema/', SpectacularAPIView.as_view(urlconf='server.urls'), name='web-schema'),
    path('web/docs/swagger/', SpectacularSwaggerView.as_view(url_name='web-schema'), name='web-swagger'),
    # path('web/', include('server.web_urls')),


   # Accounts
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # Institutions
    path('institutions/', include('institutions.urls', namespace='institutions')),

    # Appointments
    path('appointments/', include('appointments.urls', namespace='appointments')),

    # Core (regions, cities)
    path('core/', include('core.urls', namespace='core')),

    # Reviews
    path('reviews/', include('reviews.urls', namespace='reviews')),

    # Statistics (системная статистика для супер-админа)
    path('statistics/', include('statistics.urls', namespace='statistics')),

    # Notifications
    path('notifications/', include('notifications.urls', namespace='notifications')),

    # Messages / чат
    path('message/', include('message.urls', namespace='message')),

]


# from django.http import HttpResponse

# def test_view(request):
#     return HttpResponse("OK")

# urlpatterns += [path('accounts/test/', test_view)]


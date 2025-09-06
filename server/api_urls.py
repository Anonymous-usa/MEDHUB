from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.api_urls', namespace='accounts_api')),
    path('institutions/', include('institutions.api_urls', namespace='institutions_api')),
]

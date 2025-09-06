from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.web_urls', namespace='accounts_web')),
    path('institutions/', include('institutions.web_urls', namespace='institutions_web')),
    path('dashboard/', include('statistics.urls', namespace='dashboard')),

]

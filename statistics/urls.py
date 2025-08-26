from django.urls import path
from .views import OverviewStatsView, InstitutionStatsView

app_name = 'statistics'

urlpatterns = [
    path('v1/stats/overview/', OverviewStatsView.as_view(), name='stats-overview'),
    path('v1/stats/institution/<int:pk>/', InstitutionStatsView.as_view(), name='stats-institution'),
]

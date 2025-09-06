from django.urls import path

from statistics.views import AdminDashboardStatsView 



urlpatterns=[
    path('v1/dashboard/stats/', AdminDashboardStatsView.as_view(), name='dashboard-stats'),

]
# admin_custom/urls.py
from django.urls import path
from .views import dashboard_view, doctors_view, institution_detail_view, my_institution_view, my_appointments_view, my_reviews_view


urlpatterns = [
    path('dashboard/', dashboard_view, name='admin-dashboard'),
    path('doctors/', doctors_view, name='admin-doctors'),
    path('institution/<int:institution_id>/', institution_detail_view, name='admin-institution-detail'),
    path('my-institution/', my_institution_view, name='admin-my-institution'),
    path('my-appointments/', my_appointments_view, name='admin-my-appointments'),
    path('my-reviews/', my_reviews_view, name='admin-my-reviews'),
]

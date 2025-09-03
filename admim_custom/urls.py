from django.urls import path
from admim_custom import views
from .views import DepartmentListView, DepartmentDeleteView,DepartmentEditView
app_name = "admim_custom"

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("institutions/", views.institutions_view, name="institutions"),
    path("institutions/<int:institution_id>/", views.institution_detail_view, name="institution_detail"),
    path("doctors/", views.doctors_view, name="doctors"),

    # Панель учреждения
    path("my-institution/", views.my_institution_view, name="my_institution"),
    path("my-appointments/", views.my_appointments_view, name="my_appointments"),
    path("my-reviews/", views.my_reviews_view, name="my_reviews"),

    #panel otdeleniy
    path('departments/', DepartmentListView.as_view(), name='departments'),
    path('departments/<int:pk>/edit/', DepartmentEditView.as_view(), name='department-edit'),
    path('departments/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department-delete'),


    # Панель врача
    path("my-requests/", views.my_requests_view, name="my_requests"),
]


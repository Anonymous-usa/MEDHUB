from django.urls import path
from .views import (
    NotificationListView,
    NotificationMarkReadView,
    NotificationMarkAllReadView,
)

app_name = "notifications"

urlpatterns = [
    path("v1/notifications/", NotificationListView.as_view(), name="list"),
    path("v1/notifications/<int:pk>/read/", NotificationMarkReadView.as_view(), name="mark-read"),
    path("v1/notifications/read-all/", NotificationMarkAllReadView.as_view(), name="mark-all-read"),
]

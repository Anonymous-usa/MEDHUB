from django.urls import path
from .views import (
    NotificationListView,
    NotificationMarkReadView,
    NotificationMarkAllReadView,
)

app_name = "notifications"

urlpatterns = [
    path("v1/notifications/", NotificationListView.as_view(), name="list"),  # 📥 Список уведомлений
    path("v1/notifications/<int:pk>/read/", NotificationMarkReadView.as_view(), name="mark-read"),  # ✅ Одно уведомление
    path("v1/notifications/mark-all-read/", NotificationMarkAllReadView.as_view(), name="mark-all-read"),  # 📦 Все уведомления
]

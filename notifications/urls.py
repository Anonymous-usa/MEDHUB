# notifications/urls.py
from django.urls import path
from .views import (
    NotificationListView,
    NotificationMarkReadView,
    NotificationMarkAllReadView,
)

app_name = "notifications"

urlpatterns = [
    # 📥 Получить список всех уведомлений текущего пользователя
    path(
        "v1/notifications/",
        NotificationListView.as_view(),
        name="list"
    ),

    # ✅ Пометить одно уведомление как прочитанное
    path(
        "v1/notifications/<int:pk>/read/",
        NotificationMarkReadView.as_view(),
        name="mark-read"
    ),

    # 📦 Пометить все уведомления как прочитанные
    path(
        "v1/notifications/read-all/",
        NotificationMarkAllReadView.as_view(),
        name="mark-all-read"
    ),
]

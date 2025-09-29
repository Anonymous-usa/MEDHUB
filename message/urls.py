from django.urls import path
from .views import ChatView, DialogListView, MarkAsReadView

app_name = "message"

urlpatterns = [
    path("v1/dialogs/", DialogListView.as_view(), name="dialogs"),  # 🔹 Список диалогов
    path("v1/chat/<int:user_id>/", ChatView.as_view(), name="chat"),  # 🔹 История переписки и отправка сообщений
    path("v1/messages/<int:pk>/read/", MarkAsReadView.as_view(), name="mark-as-read"),  # 🔹 Пометить сообщение как прочитанное
]

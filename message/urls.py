# message/urls.py
from django.urls import path
from .views import ChatView, DialogListView, MarkAsReadView

app_name = "message"

urlpatterns = [
    # Список последних диалогов
    path("v1/dialogs/", DialogListView.as_view(), name="dialogs"),

    # История чата между текущим пользователем и указанным user_id
    path("v1/chat/<int:user_id>/", ChatView.as_view(), name="chat"),

    # Отметить конкретное сообщение как прочитанное
    path("v1/messages/<int:pk>/read/", MarkAsReadView.as_view(), name="mark-as-read"),
]

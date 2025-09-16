from django.urls import path
from .views import ChatView, DialogListView, MarkAsReadView

app_name = "message"

urlpatterns = [
    path("v1/dialogs/", DialogListView.as_view(), name="dialogs"),
    path("v1/chat/<int:user_id>/", ChatView.as_view(), name="chat"),
    path("v1/messages/<int:pk>/read/", MarkAsReadView.as_view(), name="mark-as-read"),
]

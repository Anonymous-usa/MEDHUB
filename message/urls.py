from django.urls import path
from .views import ChatView, DialogListView, MarkAsReadView

urlpatterns = [
    path("dialogs/", DialogListView.as_view(), name="dialogs"),
    path("chat/<int:user_id>/", ChatView.as_view(), name="chat"),
    path("messages/<int:pk>/read/", MarkAsReadView.as_view(), name="mark-as-read"),
]

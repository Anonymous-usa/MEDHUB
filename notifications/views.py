# notification/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsRecipient


class NotificationListView(generics.ListAPIView):
    """
    Список уведомлений текущего пользователя.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Notification.objects
            .select_related('actor', 'recipient')
            .filter(recipient=self.request.user)
            .order_by('-created_at')
        )


class NotificationMarkReadView(generics.UpdateAPIView):
    """
    Пометить одно уведомление прочитанным.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsRecipient]
    queryset = Notification.objects.all()

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=['is_read', 'updated_at'])
        return Response(
            self.get_serializer(notification).data,
            status=status.HTTP_200_OK
        )


class NotificationMarkAllReadView(generics.GenericAPIView):
    """
    Пометить все уведомления текущего пользователя прочитанными.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        qs = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        )
        updated_count = qs.update(is_read=True)
        return Response(
            {"marked_count": updated_count},
            status=status.HTTP_200_OK
        )

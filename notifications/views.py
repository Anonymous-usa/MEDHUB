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
        return Notification.objects.filter(recipient=self.request.user)

class NotificationMarkReadView(generics.UpdateAPIView):
    """
    Пометить одно уведомление прочитанным.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsRecipient]
    queryset = Notification.objects.all()

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response(self.get_serializer(notification).data, status=status.HTTP_200_OK)

class NotificationMarkAllReadView(generics.GenericAPIView):
    """
    Пометить все уведомления текущего пользователя прочитанными.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        qs = Notification.objects.filter(recipient=request.user, is_read=False)
        updated = qs.update(is_read=True)
        return Response(
            {"marked_count": updated},
            status=status.HTTP_200_OK
        )

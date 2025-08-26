from django.db.models import Q, Max
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from accounts.models import User


class DialogListView(generics.ListAPIView):
    
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        dialogs = (
            Message.objects.filter(Q(sender=user) | Q(receiver=user))
            .values("sender", "receiver")
            .annotate(last_message=Max("created_at"))
        )

        q = Q()
        for d in dialogs:
            q |= Q(created_at=d["last_message"])

        return Message.objects.filter(q).order_by("-created_at")


class ChatView(generics.ListCreateAPIView):

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.kwargs['user_id']

        return Message.objects.filter(
            Q(sender=user, receiver_id=other_user_id) |
            Q(sender_id=other_user_id, receiver=user)
        ).order_by("created_at")

    def perform_create(self, serializer):
        other_user_id = self.kwargs['user_id']
        serializer.save(sender=self.request.user, receiver_id=other_user_id)


class MarkAsReadView(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            message = Message.objects.get(pk=pk, receiver=request.user)
            message.is_read = True
            message.save()
            return Response({"status": "read"}, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

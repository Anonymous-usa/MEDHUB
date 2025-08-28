# reviews/views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Review
from .serializers import ReviewCreateSerializer, ReviewDetailSerializer
from .permissions import IsPatient


class PatientReviewListCreateView(generics.ListCreateAPIView):
    """
    GET: Список своих отзывов
    POST: Оставить новый отзыв по принятой заявке
    """
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
        return (
            Review.objects
            .select_related(
                "appointment",
                "appointment__patient",
                "appointment__doctor"
            )
            .filter(appointment__patient=self.request.user)
            .order_by("-created_at")
        )

    def get_serializer_class(self):
        return (
            ReviewCreateSerializer
            if self.request.method == "POST"
            else ReviewDetailSerializer
        )

    def get_serializer_context(self):
        return {"request": self.request}


class DoctorReviewListView(generics.ListAPIView):
    """
    GET: Список отзывов для конкретного врача
    """
    permission_classes = [AllowAny]
    serializer_class = ReviewDetailSerializer

    def get_queryset(self):
        doctor_id = self.kwargs.get("doctor_id")
        return (
            Review.objects
            .select_related(
                "appointment",
                "appointment__patient",
                "appointment__doctor"
            )
            .filter(appointment__doctor_id=doctor_id)
            .order_by("-created_at")
        )

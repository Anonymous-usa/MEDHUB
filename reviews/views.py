from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import Review
from .serializers import (
    ReviewCreateSerializer,
    ReviewDetailSerializer,
    ReviewListSerializer,
)
from .permissions import IsPatient


# 🔧 Swagger helper serializer
class ReviewPostSuccessSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    detail = serializers.CharField()


@extend_schema_view(
    get=extend_schema(
        tags=["Reviews"],
        summary="Список отзывов пациента",
        description="Возвращает список всех отзывов текущего пациента.",
        responses={200: ReviewListSerializer(many=True)},
    ),
    post=extend_schema(
        tags=["Reviews"],
        summary="Создать отзыв",
        description="Создание нового отзыва по принятой заявке. Доступно только пациенту.",
        request=ReviewCreateSerializer,
        responses={201: ReviewDetailSerializer},
    )
)
class PatientReviewListCreateView(generics.ListCreateAPIView):
    """
    Пациент может просматривать свои отзывы и создавать новые.
    """
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Review.objects.none()
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
        if self.request.method == "POST":
            return ReviewCreateSerializer
        return ReviewListSerializer

    def get_serializer_context(self):
        return {"request": self.request}


@extend_schema(
    tags=["Reviews"],
    summary="Отзывы врача",
    description="Возвращает список отзывов для конкретного врача по его ID. Доступно всем пользователям.",
    parameters=[
        OpenApiParameter(
            name="doctor_id",
            location=OpenApiParameter.PATH,
            required=True,
            type=int,
            description="ID врача"
        )
    ],
    responses={200: ReviewListSerializer(many=True)},
)
class DoctorReviewListView(generics.ListAPIView):
    """
    Любой пользователь может просматривать отзывы конкретного врача.
    """
    permission_classes = [AllowAny]
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Review.objects.none()
        doctor_id: int = self.kwargs.get("doctor_id")
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

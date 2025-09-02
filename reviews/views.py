from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import Review
from .serializers import ReviewCreateSerializer, ReviewDetailSerializer
from .permissions import IsPatient

# 🔧 Renamed Swagger helper serializer
class ReviewPostSuccessSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    detail = serializers.CharField()


@extend_schema_view(
    get=extend_schema(
        responses={200: ReviewDetailSerializer},
        description="Список отзывов текущего пациента"
    ),
    post=extend_schema(
        request=ReviewCreateSerializer,
        responses={201: ReviewDetailSerializer},
        description="Создание нового отзыва по принятой заявке"
    )
)
class PatientReviewListCreateView(generics.ListCreateAPIView):
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
        return (
            ReviewCreateSerializer
            if self.request.method == "POST"
            else ReviewDetailSerializer
        )

    def get_serializer_context(self):
        return {"request": self.request}


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="doctor_id",
            location=OpenApiParameter.PATH,
            required=True,
            type=int,
            description="ID врача"
        )
    ],
    responses={200: ReviewDetailSerializer},
    description="Список отзывов для конкретного врача"
)
class DoctorReviewListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewDetailSerializer

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

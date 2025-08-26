from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Review
from .serializers import ReviewCreateSerializer, ReviewDetailSerializer
from .permissions import IsPatient

class PatientReviewListCreateView(generics.ListCreateAPIView):
    """
    GET: список своих отзывов
    POST: оставить новый отзыв по принятой заявке
    """
    permission_classes = [IsPatient]

    def get_queryset(self):
        return Review.objects.filter(appointment__patient=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewDetailSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class DoctorReviewListView(generics.ListAPIView):
    """
    GET: список отзывов для конкретного врача
    """
    permission_classes = [AllowAny]
    serializer_class = ReviewDetailSerializer

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return Review.objects.filter(appointment__doctor_id=doctor_id).order_by('-created_at')

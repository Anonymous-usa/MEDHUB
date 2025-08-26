from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Review
from appointments.models import AppointmentRequest

class ReviewCreateSerializer(serializers.ModelSerializer):
    appointment = serializers.PrimaryKeyRelatedField(
        queryset=AppointmentRequest.objects.filter(status=AppointmentRequest.Status.ACCEPTED),
        help_text=_('ID принятой заявки на приём')
    )

    class Meta:
        model = Review
        fields = ('appointment', 'rating', 'comment')

    def validate_appointment(self, appointment):
        user = self.context['request'].user
        if appointment.patient_id != user.id:
            raise serializers.ValidationError(_('Нельзя оставить отзыв не к своей заявке'))
        return appointment

    def create(self, validated_data):
        return Review.objects.create(**validated_data)


class ReviewDetailSerializer(serializers.ModelSerializer):
    patient_phone = serializers.CharField(
        source='appointment.patient.phone_number', 
        read_only=True
    )
    doctor_phone = serializers.CharField(
        source='appointment.doctor.phone_number', 
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'appointment',
            'patient_phone',
            'doctor_phone',
            'rating',
            'comment',
            'created_at'
        )
        read_only_fields = ('id', 'created_at', 'patient_phone', 'doctor_phone')

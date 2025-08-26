from rest_framework import serializers
from .models import AppointmentRequest
from django.utils.translation import gettext_lazy as _

class AppointmentRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentRequest
        fields = ('doctor', 'note')

    def validate_doctor(self, doc):
        if doc.user_type != doc.UserType.DOCTOR:
            raise serializers.ValidationError(_('Выберите корректного врача'))
        if not doc.is_active or not doc.is_verified:
            raise serializers.ValidationError(_('Врач недоступен для приёма'))
        return doc

    def create(self, validated_data):
        user = self.context['request'].user
        return AppointmentRequest.objects.create(
            patient=user,
            **validated_data
        )

class AppointmentRequestDetailSerializer(serializers.ModelSerializer):
    patient_phone = serializers.CharField(source='patient.phone_number', read_only=True)
    doctor_phone  = serializers.CharField(source='doctor.phone_number',  read_only=True)

    class Meta:
        model = AppointmentRequest
        fields = ('id', 'patient_phone', 'doctor_phone', 'note',
                  'status', 'created_at', 'updated_at')
        read_only_fields = ('status', 'created_at', 'updated_at')

class AppointmentStatusUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=AppointmentRequest.Status.choices
    )

    class Meta:
        model = AppointmentRequest
        fields = ('status',)

    def validate_status(self, value):
        if value == AppointmentRequest.Status.PENDING:
            raise serializers.ValidationError(_('Нельзя сбросить в статус “Ожидает”'))
        return value

    def update(self, instance, validated_data):
        # При принятии заявка становится единственной у врача
        new_status = validated_data['status']
        instance.status = new_status
        instance.save()
        return instance

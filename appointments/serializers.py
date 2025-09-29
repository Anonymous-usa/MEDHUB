from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import AppointmentRequest


# 🔧 Swagger helper serializers (для документации)
class AppointmentSuccessSerializer(serializers.Serializer):
    detail = serializers.CharField()


class AppointmentErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()


class AppointmentRequestCreateSerializer(serializers.ModelSerializer):
    """
    Создание новой заявки на приём.
    Пациент указывается автоматически из request.user.
    """

    class Meta:
        model = AppointmentRequest
        fields = ('doctor', 'note')

    def validate_doctor(self, doc):
        if not doc.is_doctor():
            raise serializers.ValidationError(_('Выберите корректного врача'))
        if not doc.is_active:
            raise serializers.ValidationError(_('Врач недоступен для приёма'))
        return doc

    def create(self, validated_data):
        user = self.context['request'].user
        doctor = validated_data['doctor']

        # Проверка на существующую активную заявку
        existing = AppointmentRequest.objects.filter(
            patient=user,
            doctor=doctor,
            status=AppointmentRequest.Status.PENDING
        ).first()
        if existing:
            raise serializers.ValidationError(
                {'detail': _('У вас уже есть активная заявка к этому врачу')}
            )

        return AppointmentRequest.objects.create(patient=user, **validated_data)


class AppointmentRequestDetailSerializer(serializers.ModelSerializer):
    """
    Детальное отображение заявки.
    """
    patient_phone = serializers.CharField(source='patient.phone_number', read_only=True)
    doctor_phone = serializers.CharField(source='doctor.phone_number', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)

    class Meta:
        model = AppointmentRequest
        fields = (
            'id',
            'patient_name', 'patient_phone',
            'doctor_name', 'doctor_phone',
            'note',
            'status',
            'appointment_time',
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'status',
            'created_at',
            'updated_at',
            'patient_name', 'patient_phone',
            'doctor_name', 'doctor_phone'
        )


class AppointmentStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Обновление статуса заявки (врач/админ).
    """
    status = serializers.ChoiceField(choices=AppointmentRequest.Status.choices)

    class Meta:
        model = AppointmentRequest
        fields = ('status',)

    def validate_status(self, value):
        if value == AppointmentRequest.Status.PENDING:
            raise serializers.ValidationError(_('Нельзя сбросить в статус “Ожидает”'))
        return value

    def update(self, instance, validated_data):
        new_status = validated_data['status']
        instance.status = new_status
        instance.save()

        # Если заявка принята — все остальные активные заявки к этому врачу отклоняются
        if new_status == AppointmentRequest.Status.ACCEPTED:
            AppointmentRequest.objects.filter(
                doctor=instance.doctor,
                status=AppointmentRequest.Status.PENDING
            ).exclude(id=instance.id).update(status=AppointmentRequest.Status.REJECTED)

        return instance

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from .validators import validate_phone_number


class AccountsErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()

class AccountsSuccessSerializer(serializers.Serializer):
    detail = serializers.CharField()

class AccountsLogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class PatientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(validators=[validate_phone_number])

    class Meta:
        model = User
        fields = (
            'phone_number', 'password', 'password_confirm',
            'first_name', 'last_name', 'email', 'date_of_birth'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(
            **validated_data,
            user_type=User.UserType.PATIENT,
            password=password,
            is_verified=False
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(source='institution.name', read_only=True)

    class Meta:
        model = User
        fields = (
            'phone_number', 'first_name', 'last_name',
            'email', 'date_of_birth', 'user_type',
            'institution_name', 'is_verified'
        )
        read_only_fields = (
            'phone_number', 'user_type',
            'institution_name', 'is_verified'
        )

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


from django.utils.crypto import get_random_string

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'institution']

    def create(self, validated_data):
        validated_data['user_type'] = User.UserType.DOCTOR
        password = get_random_string(length=8)
        user = User.objects.create_user(password=password, **validated_data)
        # TODO: отправить SMS/email с паролем
        return user

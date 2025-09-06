from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import User
from accounts.validators import validate_phone_number

# 🔹 Swagger helpers
class AccountsErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()

class AccountsSuccessSerializer(serializers.Serializer):
    detail = serializers.CharField()

class AccountsLogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()

# 🔹 Регистрация пациента
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

# 🔹 Профиль пользователя
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

# 🔹 Аутентификация
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

# 🔹 Универсальная регистрация (врач, админ)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(validators=[validate_phone_number])

    class Meta:
        model = User
        fields = [
            'phone_number', 'email', 'first_name', 'last_name',
            'date_of_birth', 'user_type', 'institution',
            'password', 'password_confirm'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        request = self.context.get('request')
        if request and not request.user.is_superuser:
            if attrs.get('user_type') == User.UserType.SUPER_ADMIN:
                raise serializers.ValidationError({"user_type": "Недопустимый тип пользователя"})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

# 🔹 Для DoctorViewSet
class DoctorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'phone_number', 'date_of_birth', 'institution',
            'is_active', 'is_verified', 'password'
        ]
        read_only_fields = ['id', 'is_verified']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['user_type'] = User.UserType.DOCTOR
        user = User.objects.create_user(password=password, **validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

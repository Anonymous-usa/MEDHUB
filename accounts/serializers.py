from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'email',
            'first_name', 'last_name', 'full_name',
            'user_type', 'institution', 'is_super_admin_flag',
            'date_joined', 'last_login',
        )
        read_only_fields = ('id', 'date_joined', 'last_login', 'is_super_admin_flag')

    def get_full_name(self, obj):
        return obj.get_full_name()

class LoginRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = (
            'phone_number', 'email', 'first_name', 'last_name',
            'user_type', 'institution', 'password'
        )

    def validate(self, attrs):
        user_type = attrs.get('user_type')
        institution = attrs.get('institution')

        if user_type == User.UserType.ADMIN and not institution:
            raise serializers.ValidationError({
                'institution': _('Администратор учреждения должен быть привязан к institution')
            })

        if user_type == User.UserType.PATIENT and institution:
            raise serializers.ValidationError({
                'institution': _('Пациент не может быть привязан к institution')
            })

        if user_type == User.UserType.SUPERUSER:
            raise serializers.ValidationError({
                'user_type': _('Нельзя создать суперпользователя через обычную регистрацию')
            })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user




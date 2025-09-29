from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'phone_number', 'email',
            'first_name', 'last_name', 'full_name',
            'user_type', 'institution', 'is_super_admin_flag',
            'date_joined', 'last_login',
        )
        read_only_fields = ('id', 'date_joined', 'last_login', 'is_super_admin_flag')

    def get_full_name(self, obj):
        return obj.get_full_name()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'first_name', 'last_name', 'user_type', 'institution', 'password')

    def validate_user_type(self, value):
        allowed = {User.UserType.DOCTOR, User.UserType.PATIENT, User.UserType.ADMIN}
        if value not in allowed:
            raise serializers.ValidationError(_('Недопустимый тип пользователя'))
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

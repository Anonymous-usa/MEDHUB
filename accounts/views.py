from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, RegisterSerializer, LoginRequestSerializer

User = get_user_model()


class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Позволяет логиниться по phone_number вместо username.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'] = serializers.CharField()
        self.fields['password'] = serializers.CharField(write_only=True)
        self.fields.pop('username', None)  

    def validate(self, attrs):
        attrs['username'] = attrs['phone_number']
        return super().validate(attrs)


class LoginView(TokenObtainPairView):
    serializer_class = PhoneTokenObtainPairSerializer
    permission_classes = [AllowAny]

    @extend_schema(
    tags=["Accounts"],
    summary="Логин по номеру телефона",
    description="Авторизация пользователя по номеру телефона и паролю. "
                "Возвращает пару токенов (access и refresh).",
    request=LoginRequestSerializer  # ✅ вот это добавь
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Accounts"],
        summary="Регистрация нового пользователя",
        description="Создаёт нового пользователя в системе. Доступно без авторизации.",
        request=RegisterSerializer,
        responses={201: UserSerializer},
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Accounts"],
        summary="Профиль текущего пользователя",
        description="Возвращает данные профиля текущего авторизованного пользователя.",
        responses={200: UserSerializer},
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    @extend_schema(
        tags=["Accounts"],
        summary="Обновление профиля",
        description="Позволяет частично обновить данные профиля текущего пользователя. "
                    "Нельзя изменить роль, принадлежность к учреждению или статус супер-админа.",
        request=UserSerializer,
        responses={200: UserSerializer},
    )
    def patch(self, request):
        restricted_fields = ['user_type', 'institution', 'is_super_admin_flag']
        for field in restricted_fields:
            if field in request.data:
                raise serializers.ValidationError({field: _('Это поле нельзя изменить')})

        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

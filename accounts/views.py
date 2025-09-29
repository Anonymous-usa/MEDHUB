from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema

from .serializers import UserSerializer, RegisterSerializer


class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Позволяет логиниться по phone_number (который мы пробрасываем как username).
    """
    def validate(self, attrs):
        if 'phone_number' in attrs:
            attrs['username'] = attrs['phone_number']
        return super().validate(attrs)


class LoginView(TokenObtainPairView):
    serializer_class = PhoneTokenObtainPairSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Accounts"],
        summary="Логин по номеру телефона",
        description="Авторизация пользователя по номеру телефона и паролю. "
                    "Возвращает пару токенов (access и refresh)."
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
        description="Позволяет частично обновить данные профиля текущего пользователя.",
        request=UserSerializer,
        responses={200: UserSerializer},
    )
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

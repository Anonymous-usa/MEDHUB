import logging
from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    PatientRegistrationSerializer,
    UserProfileSerializer,
    LoginSerializer
)

logger = logging.getLogger(__name__)

class PatientRegistrationView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = PatientRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = serializer.save()
            # здесь можно отправить SMS/email для подтверждения аккаунта
            return Response({
                "detail": "Пациент успешно зарегистрирован. Подтвердите аккаунт через SMS/Email."
            }, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response(
                {"detail": "Пользователь с таким номером телефона или email уже существует."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception("Ошибка при регистрации пациента")
            return Response(
                {"detail": "Внутренняя ошибка сервера."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            return Response(
                {"detail": "Неверный номер телефона или пароль."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not user.is_active:
            return Response(
                {"detail": "Аккаунт деактивирован."},
                status=status.HTTP_403_FORBIDDEN
            )
        if not user.is_verified:
            return Response(
                {"detail": "Аккаунт не верифицирован."},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserProfileSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Токен не предоставлен."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Успешный выход из системы."}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"detail": "Неверный токен."},
                status=status.HTTP_400_BAD_REQUEST
            )

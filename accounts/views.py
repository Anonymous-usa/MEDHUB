import logging
from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

from .models import User
from .serializers import (
    PatientRegistrationSerializer,
    UserProfileSerializer,
    LoginSerializer
)
from .validators import validate_phone_number

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
            logger.info(f"Пациент зарегистрирован: {user.phone_number}")
            # TODO: отправить SMS/email для подтверждения аккаунта
            return Response({
                "detail": _("Пациент успешно зарегистрирован. Подтвердите аккаунт через SMS/Email.")
            }, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response(
                {"detail": _("Пользователь с таким номером телефона или email уже существует.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception("Ошибка при регистрации пациента")
            return Response(
                {"detail": _("Внутренняя ошибка сервера.")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = validate_phone_number(serializer.validated_data['phone_number'])
        password = serializer.validated_data['password']
        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            return Response(
                {"detail": _("Неверный номер телефона или пароль.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not user.is_active:
            return Response(
                {"detail": _("Аккаунт деактивирован.")},
                status=status.HTTP_403_FORBIDDEN
            )
        if not user.is_verified:
            return Response(
                {"detail": _("Аккаунт не верифицирован.")},
                status=status.HTTP_403_FORBIDDEN
            )

        logger.info(f"Пользователь вошёл: {user.phone_number}")
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
        if not request.user.is_patient():
            return Response(
                {"detail": _("Редактирование профиля доступно только пациентам.")},
                status=status.HTTP_403_FORBIDDEN
            )
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
                {"detail": _("Токен не предоставлен.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": _("Успешный выход из системы.")}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"detail": _("Неверный токен.")},
                status=status.HTTP_400_BAD_REQUEST
            )

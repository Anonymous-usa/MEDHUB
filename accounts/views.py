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

from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

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
    serializer_class = PatientRegistrationSerializer

    @extend_schema(
        request=PatientRegistrationSerializer,
        responses={201: OpenApiTypes.OBJECT},
        description="Регистрация нового пациента"
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = serializer.save()
            logger.info(f"Пациент зарегистрирован: {user.phone_number}")
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
    throttle_scope = 'login'
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT},
        description="Аутентификация пользователя"
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Login failed: invalid input — {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = validate_phone_number(serializer.validated_data['phone_number'])
        password = serializer.validated_data['password']
        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            logger.warning(f"Login failed: invalid credentials for {phone_number}")
            return Response(
                {"detail": _("Неверный номер телефона или пароль.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not user.is_active:
            logger.warning(f"Login blocked: inactive account {phone_number}")
            return Response(
                {"detail": _("Аккаунт деактивирован.")},
                status=status.HTTP_403_FORBIDDEN
            )
        if not user.is_verified:
            logger.warning(f"Login blocked: unverified account {phone_number}")
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
    throttle_scope = 'profile'
    serializer_class = UserProfileSerializer

    @extend_schema(
        responses=UserProfileSerializer,
        description="Получение профиля текущего пользователя"
    )
    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    @extend_schema(
        request=UserProfileSerializer,
        responses=UserProfileSerializer,
        description="Обновление профиля пациента"
    )
    def put(self, request):
        if not request.user.is_patient():
            logger.warning(f"Profile edit blocked for non-patient: {request.user}")
            return Response(
                {"detail": _("Редактирование профиля доступно только пациентам.")},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Профиль обновлён: {request.user.phone_number}")
            return Response(serializer.data)

        logger.warning(f"Profile update failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
        description="Выход из системы"
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            logger.warning("Logout failed: no token provided")
            return Response(
                {"detail": _("Токен не предоставлен.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"Токен отозван: {refresh_token}")
            return Response({"detail": _("Успешный выход из системы.")}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Ошибка при выходе из системы")
            return Response(
                {"detail": _("Неверный токен.")},
                status=status.HTTP_400_BAD_REQUEST
            )

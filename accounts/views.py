import logging
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import status, serializers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema, extend_schema_view

from accounts.models import User
from accounts.serializers import (
    PatientRegistrationSerializer,
    UserProfileSerializer,
    LoginSerializer,
    AccountsLogoutRequestSerializer,
    AccountsErrorSerializer,
    AccountsSuccessSerializer,
    DoctorSerializer
)
from accounts.validators import validate_phone_number

logger = logging.getLogger(__name__)


# 🔹 Регистрация пациента
class PatientRegistrationView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    serializer_class = PatientRegistrationSerializer

    @extend_schema(
        request=PatientRegistrationSerializer,
        responses={201: AccountsSuccessSerializer, 400: AccountsErrorSerializer, 500: AccountsErrorSerializer},
        description="Регистрация нового пациента"
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
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
        except Exception:
            logger.exception("Ошибка при регистрации пациента")
            return Response(
                {"detail": _("Внутренняя ошибка сервера.")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# 🔹 Аутентификация
class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    throttle_scope = 'login'
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        responses={200: UserProfileSerializer, 400: AccountsErrorSerializer, 403: AccountsErrorSerializer},
        description="Аутентификация пользователя"
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Login failed: invalid input — {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = validate_phone_number(serializer.validated_data['phone_number'])
        password = serializer.validated_data['password']
        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            logger.warning(f"Login failed: invalid credentials for {phone_number}")
            return Response({"detail": _("Неверный номер телефона или пароль.")}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            logger.warning(f"Login blocked: inactive account {phone_number}")
            return Response({"detail": _("Аккаунт деактивирован.")}, status=status.HTTP_403_FORBIDDEN)
        if not user.is_verified:
            logger.warning(f"Login blocked: unverified account {phone_number}")
            return Response({"detail": _("Аккаунт не верифицирован.")}, status=status.HTTP_403_FORBIDDEN)

        logger.info(f"Пользователь вошёл: {user.phone_number}")
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserProfileSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)


# 🔹 Профиль пользователя
class UserProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = 'profile'
    serializer_class = UserProfileSerializer

    @extend_schema(
        responses={200: UserProfileSerializer},
        description="Получение профиля текущего пользователя"
    )
    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer, 400: AccountsErrorSerializer, 403: AccountsErrorSerializer},
        description="Обновление профиля пациента"
    )
    def put(self, request):
        if not request.user.is_patient():
            logger.warning(f"Profile edit blocked for non-patient: {request.user}")
            return Response(
                {"detail": _("Редактирование профиля доступно только пациентам.")},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Профиль обновлён: {request.user.phone_number}")
            return Response(serializer.data)

        logger.warning(f"Profile update failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 Выход из системы
class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountsLogoutRequestSerializer

    @extend_schema(
        request=AccountsLogoutRequestSerializer,
        responses={200: AccountsSuccessSerializer, 400: AccountsErrorSerializer},
        description="Выход из системы"
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            logger.warning("Logout failed: no token provided")
            return Response({"detail": _("Токен не предоставлен.")}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"Токен отозван: {refresh_token}")
            return Response({"detail": _("Успешный выход из системы.")}, status=status.HTTP_200_OK)
        except Exception:
            logger.exception("Ошибка при выходе из системы")
            return Response({"detail": _("Неверный токен.")}, status=status.HTTP_400_BAD_REQUEST)


# 🔹 Управление врачами
@extend_schema_view(
    list=extend_schema(description="Список врачей"),
    retrieve=extend_schema(description="Детали врача"),
    create=extend_schema(description="Создание врача"),
    update=extend_schema(description="Обновление врача"),
    partial_update=extend_schema(description="Частичное обновление врача"),
    destroy=extend_schema(description="Удаление врача"),
)
class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return User.objects.filter(user_type=User.UserType.DOCTOR)
        elif user.is_institution_admin():
            return User.objects.filter(user_type=User.UserType.DOCTOR, institution=user.institution)
        elif user.is_doctor():
            return User.objects.filter(id=user.id)
        return User.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_institution_admin():
            serializer.save(institution=user.institution, user_type=User.UserType.DOCTOR)
        else:
            serializer.save(user_type=User.UserType.DOCTOR)

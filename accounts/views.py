"""
accounts/views.py

Account-related API endpoints, following best practices for Django REST Framework.
Views: PatientRegistrationView, LoginView, UserProfileView, LogoutView.
"""

import logging
from typing import Any

from django.contrib.auth import logout as django_logout
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import (
    PatientRegistrationSerializer,
    UserProfileSerializer,
    CustomAuthTokenSerializer,
)

logger = logging.getLogger(__name__)


class PatientRegistrationView(generics.CreateAPIView):
    """
    API endpoint for registering a new patient account.
    Allows unauthenticated access. On successful registration, returns user data (minus write-only fields).

    Expected payload:
    {
        "username": "string",
        "email": "string",
        "password": "string",
        ... (other fields as required)
    }
    """

    serializer_class = PatientRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer: PatientRegistrationSerializer) -> None:
        """
        Save the new user and optionally log registration.
        """
        user = serializer.save()
        logger.info("New user registered: %s (id=%s)", user.username, user.pk)


class LoginView(ObtainAuthToken):
    """
    API endpoint for obtaining an authentication token.
    Accepts username and password (can be adapted to support email login).
    Returns a DRF auth token and user details on success.
    """

    serializer_class = CustomAuthTokenSerializer  # Supports username/email login, see serializers.py
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Authenticate the user and return token.
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        logger.info("User login successful: %s (id=%s)", user.username, user.pk)
        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.pk,
                    "username": user.username,
                    "email": user.email,
                    # Add other fields as desired...
                }
            },
            status=status.HTTP_200_OK
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the authenticated user's profile.
    Authentication required.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> Any:
        """
        Retrieve the user instance for the current request.
        """
        return self.request.user

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Return the current user's profile data.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Update the current user's profile with validated data.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("User profile updated: %s (id=%s)", instance.username, instance.pk)
        return Response(serializer.data)


class LogoutView(APIView):
    """
    API endpoint for logging out the current user.
    For token authentication, deletes the user's token.
    For session authentication, calls Django logout.
    Only available to authenticated users.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Log out the current user. For token-auth, deletes the token; for session-auth, calls Django logout.
        """
        user = request.user
        auth = getattr(request, 'auth', None)

        # Token auth: delete the token
        if isinstance(auth, Token):
            try:
                auth.delete()
                logger.info("User logged out (token deleted): %s (id=%s)", user.username, user.pk)
            except Exception as e:
                logger.error("Failed to delete auth token for user %s: %s", user.username, e)
                return Response(
                    {"detail": _("Failed to log out. Please try again.")},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            # Session auth: call Django logout
            django_logout(request)
            logger.info("User logged out (session): %s (id=%s)", user.username, user.pk)

        return Response({"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK)
# from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# class JWTLogoutView(APIView):
#     """
#     API endpoint for logging out a JWT-authenticated user.
#     Blacklists the provided refresh token.
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request: Request) -> Response:
#         refresh_token = request.data.get('refresh')
#         if not refresh_token:
#             return Response({"detail": _("Refresh token required.")}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             logger.info("JWT refresh token blacklisted for user %s", request.user.username)
#             return Response({"detail": _("Successfully logged out.")}, status=status.HTTP_205_RESET_CONTENT)
#         except TokenError as e:
#             logger.error("JWT token blacklist error: %s", e)
#             return Response({"detail": _("Invalid or already blacklisted token.")}, status=status.HTTP_400_BAD_REQUEST)

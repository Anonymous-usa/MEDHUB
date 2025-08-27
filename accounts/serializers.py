"""
Serializers for the accounts application.

This module defines and documents DRF serializers used for user registration,
authentication, and profile management. All serializers adhere to current best
practices for Django REST Framework, leveraging type annotations, docstrings,
and DRY field declarations.
"""

from typing import Any, Dict

from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import Patient, UserProfile

__all__ = [
    "PatientRegistrationSerializer",
    "UserProfileSerializer",
    "LoginSerializer",
]


class PatientRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new patient.

    Adds secure password handling and optional password confirmation.
    Ensures password is write-only and securely hashed. Designed to
    utilize Patient model's custom manager (e.g., `create_user`).
    """

    password: serializers.CharField = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        help_text="Password for the new account (minimum 8 characters)."
    )
    confirm_password: serializers.CharField = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        help_text="Repeat password to confirm."
    )

    class Meta:
        model = Patient
        # Adjust fields as suitable for your Patient model.
        fields = [
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "date_of_birth": {"required": True},
        }

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that password and confirm_password match.
        """
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        # Any additional validation (e.g., on email) can be done here.
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Patient:
        """
        Creates a new Patient with secure password hashing.
        Removes confirm_password field after validation.
        """
        validated_data.pop("confirm_password")
        patient = Patient.objects.create_user(**validated_data)
        return patient


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile representation.

    Wraps the UserProfile model, securing sensitive fields.
    Provides a clean read-write contract for end-user profile data.
    Adjust fields as appropriate for your actual UserProfile model.
    """

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "phone_number",
            "address",
            "birth_date",
        ]
        read_only_fields = ["user"]


class LoginSerializer(serializers.Serializer):
    """
    Serializer for authenticating user credentials (login).

    Accepts login fields, validates that a matching user exists,
    and adds the authenticated user to `validated_data["user"]`
    attribute on success. Use the resulting user in view or service layers.
    """

    email: serializers.EmailField = serializers.EmailField(
        help_text="Email address for login."
    )
    password: serializers.CharField = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        help_text="Password for login."
    )

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempts to authenticate the user using the provided credentials.

        Returns:
            dict: attrs with the authenticated user instance at attrs["user"].
        Raises:
            serializers.ValidationError: If authentication fails.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")

        attrs["user"] = user
        return attrs


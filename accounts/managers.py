"""
Custom user manager for phone number-based Django user authentication.

This module provides a robust, well-documented implementation of a custom UserManager
that normalizes phone numbers, securely creates users, and enforces field validation
and uniqueness. Integrates cleanly with Django admin and management commands.

Author: Accounts Team
"""

import logging
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _

try:
    import phonenumbers
    from phonenumbers.phonenumberutil import NumberParseException
except ImportError:
    phonenumbers = None

logger = logging.getLogger(__name__)

class CustomUserManager(BaseUserManager):
    """
    Custom user manager that creates users using a normalized phone number and email.

    This manager ensures:
        - Unique, normalized phone numbers (in E.164 format)
        - Uniqueness and normalization for emails
        - Secure password handling (all passwords are hashed)
        - Robust error handling for all user creation workflows
        - Clean integration with custom user models and Django admin

    Usage:
        In your custom user model, set:
            objects = CustomUserManager()
    """

    use_in_migrations = True

    def _normalize_phone_number(self, phone_number: str, region: str = "US") -> str:
        """
        Normalize and validate a phone number to E.164 format.

        Args:
            phone_number (str): User-provided phone number.
            region (str): Optional default region for parsing numbers without country code.

        Returns:
            str: Phone number in E.164 format.

        Raises:
            ValidationError: If the phone number is invalid, missing, or improperly formatted.
        """
        if not phone_number:
            raise ValidationError(_("Phone number is required."))
        if not phonenumbers:
            logger.error("phonenumbers library is required for phone number normalization.")
            raise ValidationError(_("Phone number normalization failed: contact system administrator."))

        try:
            parsed_number = phonenumbers.parse(phone_number, region)
            if not phonenumbers.is_possible_number(parsed_number) or not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError(_("The provided phone number is invalid."))
            normalized = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            return normalized
        except NumberParseException as exc:
            logger.info("Phone number parsing failed: %s", exc)
            raise ValidationError(_("Invalid phone number format: %(msg)s"), params={"msg": exc})

    def create_user(self, phone_number: str, email: str, password: str = None, **extra_fields):
        """
        Create and save a user with the given phone number, email, and password.

        Args:
            phone_number (str): The user's phone number (required).
            email (str): The user's email address (required).
            password (str): The user's password (required by default).
            **extra_fields: Additional fields to set on the user.

        Returns:
            CustomUser: The created user instance.

        Raises:
            ValidationError: If required fields are missing or invalid.
            IntegrityError: If phone_number or email already exists.
        """
        if not phone_number:
            raise ValidationError(_("The phone number must be set."))
        if not email:
            raise ValidationError(_("The email address must be set."))

        # Normalize and validate phone number and email
        normalized_phone = self._normalize_phone_number(phone_number)
        normalized_email = self.normalize_email(email)

        # Enforce uniqueness at the application layer before database save attempt
        model_class = self.model
        if model_class.objects.filter(phone_number=normalized_phone).exists():
            raise ValidationError(_("A user with this phone number already exists."))
        if model_class.objects.filter(email__iexact=normalized_email).exists():
            raise ValidationError(_("A user with this email address already exists."))

        user = model_class(
            phone_number=normalized_phone,
            email=normalized_email,
            **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        try:
            user.save(using=self._db)
        except IntegrityError as exc:
            logger.warning("Database constraint violation on user save: %s", exc)
            raise ValidationError(_("User creation failed due to duplicate or invalid data."))
        return user

    def create_superuser(self, phone_number: str, email: str, password: str = None, **extra_fields):
        """
        Create and save a superuser with the given phone number, email, and password.

        Args:
            phone_number (str): Phone number.
            email (str): Email address.
            password (str): Password (required).
            **extra_fields: Additional fields.

        Returns:
            CustomUser: The created superuser instance.

        Raises:
            ValidationError: If required fields or flags are missing/incorrect.
        """
        if not password:
            raise ValidationError(_("A password is required for superusers."))

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValidationError(_("Superuser must have is_staff=True."))
        if not extra_fields.get('is_superuser'):
            raise ValidationError(_("Superuser must have is_superuser=True."))
        if not extra_fields.get('is_active'):
            raise ValidationError(_("Superuser must have is_active=True."))

        return self.create_user(phone_number, email, password, **extra_fields)

    def get_by_natural_key(self, phone_number: str):
        """
        Fetch a user by natural key (used for authentication backend lookups).

        Args:
            phone_number (str): The normalized phone number.

        Returns:
            CustomUser: The user instance matching the phone number.

        Raises:
            CustomUser.DoesNotExist: If the user does not exist.
        """
        normalized_phone = self._normalize_phone_number(phone_number)
        return self.get(phone_number=normalized_phone)

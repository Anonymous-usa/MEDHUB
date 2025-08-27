"""
Custom Django authentication backend for phone number authentication.

This module defines the PhoneNumberBackend class, which enables authentication of
users using their phone number instead of, or in addition to, traditional usernames.
It follows Django best practices for custom authentication backends
and leverages django-phonenumber-field for robust international number validation.

References:
- https://docs.djangoproject.com/en/5.2/topics/auth/customizing/
- https://github.com/stefanfoulis/django-phonenumber-field
- https://www.geeksforgeeks.org/python/customizing-phone-number-authentication-in-django/
- https://pypi.org/project/django-phonenumber-field/
"""

from typing import Optional
import logging

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned, PermissionDenied
from phonenumber_field import PhoneNumber



logger = logging.getLogger(__name__)

class PhoneNumberBackend(BaseBackend):
    """
    Authenticate users using their phone number and password.

    This authentication backend allows users to use their registered phone number
    for login instead of (or in addition to) the default username/email field.
    It requires that the custom user model has a unique `phone_number` field,
    recommended as a PhoneNumberField from django-phonenumber-field.

    Example usage (in forms):

        user = authenticate(request, phone_number='+15551234567', password='secret')
        if user is not None:
            login(request, user)

    Note:
        This backend assumes the user model defines a unique `phone_number`,
        and that passwords are set and checked via Django's password hashing system.
    """

    def authenticate(
        self,
        request,
        phone_number: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs
    ) -> Optional[object]:
        """
        Authenticate a user using a phone number and password.

        Parameters:
            request: Optional[HttpRequest]. The current request (may be None).
            phone_number: str. The phone number to authenticate with.
            password: str. The password associated with the phone number.
            **kwargs: Additional keyword arguments (ignored).

        Returns:
            The authenticated user object if successful, or None.
        """
        UserModel = get_user_model()

        if phone_number is None or password is None:
            return None

        # Normalize and validate the phone number using the model's field
        try:
            # Convert to E.164 format using PhoneNumberField's validation.
            phone_number_obj = PhoneNumber.from_string(phone_number)
        except Exception as exc:
            logger.warning(
                "Failed to parse phone number '%s': %s", phone_number, exc
            )
            return None

        try:
            # Use the field name dynamically to support user model swaps.
            field_name = getattr(UserModel, "USERNAME_FIELD", "phone_number")
            user_query = {field_name: phone_number_obj}
            user = UserModel.objects.get(**user_query)
        except UserModel.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            # This should never occur if phone_number is unique
            logger.error(
                "Multiple users found with the same phone number: %s", phone_number
            )
            return None
        except Exception as exc:
            logger.exception("Unexpected error during phone auth: %s", exc)
            return None

        # Ensure user is_active is True and the password matches
        if not getattr(user, "is_active", True):
            logger.warning(
                "Attempted login for inactive user with phone number '%s'.", phone_number
            )
            return None

        # Use the user's check_password method to avoid timing attacks
        if hasattr(user, 'check_password'):
            password_valid = user.check_password(password)
        else:
            # Fallback (should not be needed if using AbstractBaseUser)
            password_valid = check_password(password, user.password)

        if not password_valid:
            logger.info(
                "Failed authentication attempt for phone number '%s': invalid password.",
                phone_number
            )
            return None

        return user

    def get_user(self, user_id: int) -> Optional[object]:
        """
        Retrieve a user instance by primary key.

        Parameters:
            user_id: int. The primary key of the user.

        Returns:
            The user object if found, else None.
        """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


"""
accounts/validators.py

Custom validators for the accounts app.

This module provides a validator for Tajikistan phone numbers, 
enforcing the correct format using Django's validation framework.

Author: [Your Name]
Last Updated: Aug 2025
"""

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Regular expression for a valid Tajikistan phone number in E.164 format
# Examples of valid formats:
#   +992900123456   (mobile)
#   +992372123456   (Dushanbe landline)
# Accepts:
#   - Leading '+'
#   - 12 or 13 digits in total (including country code), depending on area code
TAJIK_PHONE_REGEX = re.compile(r'^\+992\d{9,10}$')


def validate_phone_number(value):
    """
    Validate a Tajikistan phone number.

    The number must:
      - Start with '+992'
      - Be followed by 9 or 10 digits (mobile or landline, depending on region)
      - Contain only digits after the country code
      - Not contain spaces, hyphens, or other non-digit characters
    Examples of valid numbers:
      - +992900123456  (mobile)
      - +992372123456  (Dushanbe landline)

    Args:
        value (str): The input phone number string.

    Raises:
        ValidationError: If the phone number does not match the required format.
    """
    # Normalize input: Trim spaces, ensure string type
    if value is None:
        raise ValidationError(
            _("Phone number field value cannot be None."),
            code="invalid_phone_number",
            params={'value': value},
        )

    value = value.strip()
    if not value:
        # If the field is required, this will be caught by 'required' validation elsewhere.
        # We do not raise here unless empty numbers should be forbidden at this validator level.
        return

    # Check for any disallowed characters (anything except digits and first '+')
    if not re.fullmatch(r'\+?\d+', value):
        raise ValidationError(
            _("Phone number can only contain digits and an optional leading '+'."),
            code="invalid_characters",
            params={'value': value},
        )

    # Enforce the specific Tajikistan format
    if not TAJIK_PHONE_REGEX.fullmatch(value):
        raise ValidationError(
            _("Enter a valid Tajikistan phone number in the format: '+992XXXXXXXXX'."),
            code="invalid_phone_number",
            params={'value': value},
        )

    # Additional logic (optional): Forbid obvious mistakes (e.g., repeated country codes, etc.)
    # Further normalization, cleaning, or uniqueness checking can be done at the form/model level.


class TajikistanPhoneNumberValidator:
    """
    Validator class for Tajikistan phone numbers.

    This class-based validator enables direct use with Django model and form fields,
    allowing migration serialization and advanced customization.

    Attributes:
        message (str): Error message template.
        code (str): Error code for failed validations.

    Usage:
        from accounts.validators import TajikistanPhoneNumberValidator

        phone = models.CharField(
            validators=[TajikistanPhoneNumberValidator()],
            max_length=13,
        )
    """

    message = _("Enter a valid Tajikistan phone number in the format: '+992XXXXXXXXX'.")
    code = 'invalid_phone_number'
    regex = TAJIK_PHONE_REGEX

    def __call__(self, value):
        """
        Validate input against the Tajikistan phone number format.

        Args:
            value (str): Phone number to validate.

        Raises:
            ValidationError: If the number does not match.
        """
        if value is None:
            raise ValidationError(
                _("Phone number field value cannot be None."),
                code=self.code,
                params={'value': value},
            )

        clean = str(value).strip()
        if not clean:
            return  # Leave 'required' or blank checks to forms/fields.

        if not re.fullmatch(r'\+?\d+', clean):
            raise ValidationError(
                _("Phone number can only contain digits and an optional leading '+'."),
                code="invalid_characters",
                params={'value': value},
            )

        if not self.regex.fullmatch(clean):
            raise ValidationError(
                self.message,
                code=self.code,
                params={'value': value},
            )

    def __eq__(self, other):
        return (
            isinstance(other, TajikistanPhoneNumberValidator)
            and self.message == other.message
            and self.code == other.code
            and self.regex.pattern == other.regex.pattern
        )

    def deconstruct(self):
        """
        Deconstruction method for Django migrations compatibility.
        """
        return (
            f'{self.__class__.__module__}.{self.__class__.__name__}',
            [],
            {
                'message': self.message,
                'code': self.code,
            },
        )


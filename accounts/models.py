# accounts/models.py

"""
Custom User model for the accounts app based on AbstractUser.
- Uses phone_number as the unique identifier (`USERNAME_FIELD`).
- Supports role handling with TextChoices.
- Includes email, date_of_birth, institution reference, and verification flags.
- Inherits created_at and updated_at timestamps via abstract TimeStampedModel.
- Implements clean field validation, type annotations, indexes, and docstring formatting.
"""

from typing import Any, Optional

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator, validate_email
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    Abstract base class that adds created_at and updated_at timestamp fields
    to any inheriting model.
    """
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
        help_text=_("The datetime when this record was created."),
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
        help_text=_("The datetime when this record was last updated."),
    )

    class Meta:
        abstract = True


class UserType(models.TextChoices):
    """
    Enumerates possible user roles for role-based access control.
    """
    ADMIN = "ADMIN", _("Admin")
    STAFF = "STAFF", _("Staff")
    TEACHER = "TEACHER", _("Teacher")
    STUDENT = "STUDENT", _("Student")
    # Add additional roles as needed.


def phone_number_validator():
    """
    Returns a validator that ensures phone numbers conform to E.164 international standard.
    Example: +12345678901 (up to 15 digits)
    """
    return RegexValidator(
        regex=r'^\+?\d{9,15}$',
        message=_(
            "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        ),
    )


def validate_not_future(value):
    """
    Validator for date_of_birth to ensure date is not in the future.
    """
    if value > timezone.now().date():
        raise models.ValidationError(_("Date of birth cannot be in the future."))


class UserManager(BaseUserManager["User"]):
    """
    Custom user manager for User model: supports creation using phone_number
    and handles normalization, validation, and superuser flags.
    """

    use_in_migrations = True

    def create_user(
        self,
        phone_number: str,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> "User":
        """
        Create and save a regular User using the phone number as the unique identifier.
        """
        if not phone_number:
            raise ValueError(_("The phone number must be set."))

        # Validate the phone number using E.164 regex
        phone_number_cleaned = self.normalize_phone(phone_number)
        extra_fields.setdefault('is_active', True)
        user = self.model(phone_number=phone_number_cleaned, **extra_fields)
        user.set_password(password)
        user.full_clean()  # Validate against model field/validators
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        phone_number: str,
        password: str,
        **extra_fields: Any
    ) -> "User":
        """
        Create and save a SuperUser using the phone number as unique identifier.
        """
        extra_fields.setdefault('user_type', UserType.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_("Superuser must have is_superuser=True."))
        if extra_fields.get('user_type') != UserType.ADMIN:
            raise ValueError(_("Superuser must have user_type=ADMIN."))

        return self.create_user(phone_number, password, **extra_fields)

    @staticmethod
    def normalize_phone(phone: str) -> str:
        """
        Normalize phone number by stripping whitespace and ensuring leading '+'.
        """
        phone = phone.strip()
        if not phone.startswith("+"):
            phone = "+" + phone
        return phone


class Institution(models.Model):
    """
    Placeholder Institution model for relation. Replace or extend as needed.
    """
    name: models.CharField = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_("institution name"),
    )

    def __str__(self):
        return self.name


class User(AbstractUser, TimeStampedModel):
    """
    Custom User model with phone_number as the unique identifier, role field,
    and additional profile data.
    """

    username = None  # Remove username field completely

    # Roles / User types
    user_type: models.CharField = models.CharField(
        max_length=16,
        choices=UserType.choices,
        default=UserType.STUDENT,
        verbose_name=_("role"),
        help_text=_("Role or type of this user (admin, staff, student, etc)."),
        db_index=True,
    )

    # Phone Number
    phone_number: models.CharField = models.CharField(
        max_length=16,
        unique=True,
        validators=[phone_number_validator()],
        verbose_name=_("phone number"),
        help_text=_("Unique phone number, used for login. Format: '+999999999'."),
        db_index=True,
    )

    # Email (required, unique, case-insensitive constraint recommended)
    email: models.EmailField = models.EmailField(
        unique=True,
        validators=[validate_email],
        verbose_name=_("email address"),
        help_text=_("User's email address. Must be unique."),
        error_messages={
            "unique": _("A user with that email already exists."),
        },
        db_index=True,
    )

    # Date of birth
    date_of_birth: models.DateField = models.DateField(
        null=True,
        blank=True,
        validators=[validate_not_future],
        verbose_name=_("date of birth"),
        help_text=_("User's date of birth."),
    )

    # Institution (optional FK)
    institution: models.ForeignKey = models.ForeignKey(
        Institution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name=_("institution"),
        help_text=_("Institution the user is affiliated with."),
    )

    # Is the user's phone or email verified
    is_verified: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name=_("is verified"),
        help_text=_("Designates whether this user has completed verification."),
    )

    # Timestamps provided by TimeStampedModel (created_at, updated_at)

    # Permissions flags, names retained for compatibility
    is_active: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name=_("active"),
        help_text=_(
            "Designates whether this user should be treated as active. Unselect to deactivate."
        ),
    )
    is_staff: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name=_("staff status"),
        help_text=_("Designates whether the user can log into this admin site."),
    )

    # Set the unique login field and required fields
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    # Attach the custom user manager
    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        indexes = [
            models.Index(fields=["phone_number"], name="user_phone_idx"),
            models.Index(fields=["email"], name="user_email_idx"),
            models.Index(fields=["user_type"], name="user_user_type_idx"),
        ]
        unique_together = (
            ("phone_number", "email"),
        )
        constraints = [
            # For PostgreSQL, consider adding
            # models.UniqueConstraint(Lower('email'), name="user_email_ci_unique"),
        ]

    def __str__(self) -> str:
        """
        String representation for admin and shell.
        """
        return f"{self.phone_number} ({self.get_user_type_display()})"

    # --- Role convenience properties

    @property
    def is_admin(self) -> bool:
        return self.user_type == UserType.ADMIN

    @property
    def is_teacher(self) -> bool:
        return self.user_type == UserType.TEACHER

    @property
    def is_student(self) -> bool:
        return self.user_type == UserType.STUDENT

    @property
    def is_staff_user(self) -> bool:
        return self.user_type == UserType.STAFF

    def clean(self):
        """
        Extra model-level validation.
        """
        super().clean()
        # Enforce lowercase for emails for uniqueness (if not using CIEmailField).
        if self.email:
            self.email = self.email.lower()

    # Optionally, add age calculation helper
    @property
    def age(self) -> Optional[int]:
        """
        Returns the user's age in years, or None if date_of_birth is not set.
        """
        if self.date_of_birth is None:
            return None
        today = timezone.now().date()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


# Register this user model as AUTH_USER_MODEL in your settings:
# AUTH_USER_MODEL = 'accounts.User'


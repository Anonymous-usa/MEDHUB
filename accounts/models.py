from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .managers import CustomUserManager
from .validators import validate_phone_number


class User(AbstractUser):
    class UserType(models.TextChoices):
        PATIENT = 'patient', _('Пациент')
        DOCTOR = 'doctor', _('Врач')
        INSTITUTION_ADMIN = 'institution_admin', _('Администратор учреждения')
        SUPER_ADMIN = 'super_admin', _('Супер администратор')

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.PATIENT,
        db_index=True
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        verbose_name=_("Номер телефона"),
        validators=[validate_phone_number]
    )
    email = models.EmailField(_("Email"), unique=True)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_("Дата рождения"))

    institution = models.ForeignKey(
        'institutions.Institution',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff',
        db_index=True
    )

    is_verified = models.BooleanField(default=False, verbose_name=_("Верифицирован"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активен"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.phone_number} ({self.get_full_name()})"

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def clean(self):
        if self.user_type in [self.UserType.DOCTOR, self.UserType.INSTITUTION_ADMIN] and not self.institution:
            raise ValidationError(_("Доктор и администратор учреждения должны быть привязаны к учреждению."))
        if self.user_type == self.UserType.PATIENT and self.institution:
            raise ValidationError(_("Пациент не должен быть привязан к учреждению."))

    # Хелперы по ролям
    def is_patient(self):
        return self.user_type == self.UserType.PATIENT

    def is_doctor(self):
        return self.user_type == self.UserType.DOCTOR

    def is_institution_admin(self):
        return self.user_type == self.UserType.INSTITUTION_ADMIN

    def is_super_admin(self):
        return self.user_type == self.UserType.SUPER_ADMIN

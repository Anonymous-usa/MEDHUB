from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from institutions.models import Institution
from .managers import CustomUserManager
from .validators import validate_phone_number


class User(AbstractUser):
    class UserType(models.TextChoices):
        ADMIN = 'admin', _('Institution Admin')
        DOCTOR = 'doctor', _('Doctor')
        PATIENT = 'patient', _('Patient')
        STAFF = 'staff', _('Staff')

    # Логин по телефону
    phone_number = models.CharField(
        max_length=32,
        unique=True,
        validators=[validate_phone_number],
        verbose_name=_('Phone number'),
        help_text=_('E.164 format preferred (+992...)')
    )

    # Ролевая принадлежность
    user_type = models.CharField(
        max_length=16,
        choices=UserType.choices,
        verbose_name=_('User type')
    )

    # Привязка к учреждению (для админов/врачей/персонала)
    institution = models.ForeignKey(
        Institution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff',
        verbose_name=_('Institution'),
    )

    # Глобальная супер‑админ роль
    is_super_admin_flag = models.BooleanField(
        default=False,
        verbose_name=_('Is super admin'),
        help_text=_('System-wide super admin with full access')
    )

    # Подключаем кастомный менеджер
    objects = CustomUserManager()

    REQUIRED_FIELDS = ['phone_number', 'email', 'user_type']

    def get_full_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.username

    # Централизованные ролевые методы
    def is_super_admin(self) -> bool:
        return bool(self.is_super_admin_flag)

    def is_institution_admin(self) -> bool:
        return self.user_type == self.UserType.ADMIN

    def is_doctor(self) -> bool:
        return self.user_type == self.UserType.DOCTOR

    def is_patient(self) -> bool:
        return self.user_type == self.UserType.PATIENT

    def __str__(self):
        role = self.get_user_type_display() if self.user_type else 'Unknown'
        inst = f" @ {self.institution_id}" if self.institution_id else ""
        return f"{self.get_full_name()} [{role}]{inst}"

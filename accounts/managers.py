from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import re

class CustomUserManager(BaseUserManager):
    def normalize_phone_number(self, phone_number):
        phone_number = re.sub(r'[\s\-\(\)]', '', phone_number)
        if phone_number.startswith('0') and len(phone_number) == 10:
            phone_number = '+992' + phone_number[1:]
        return phone_number

    def create_user(self, phone_number, email, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('Номер телефона обязателен'))
        if not email:
            raise ValueError(_('Email обязателен'))
        if not password:
            raise ValueError(_('Пароль обязателен'))

        phone_number = self.normalize_phone_number(phone_number)
        email = self.normalize_email(email)

        user_type = extra_fields.get('user_type', self.model.UserType.PATIENT)
        institution = extra_fields.get('institution', None)

        if user_type in [self.model.UserType.DOCTOR, self.model.UserType.INSTITUTION_ADMIN] and not institution:
            raise ValueError(_('Доктор и администратор учреждения должны быть привязаны к учреждению'))
        if user_type == self.model.UserType.PATIENT and institution:
            raise ValueError(_('Пациент не должен быть привязан к учреждению'))

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', False)

        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('user_type', self.model.UserType.SUPER_ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперадмин должен иметь is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперадмин должен иметь is_superuser=True'))

        return self.create_user(phone_number, email, password, **extra_fields)

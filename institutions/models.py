# institutions/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Institution(models.Model):
    class InstitutionType(models.TextChoices):
        HOSPITAL    = 'hospital',    _('Больница')
        CLINIC      = 'clinic',      _('Клиника')
        LABORATORY  = 'laboratory',  _('Лаборатория')
        OTHER       = 'other',       _('Другое')

    class OwnershipType(models.TextChoices):
        STATE   = 'state',   _('Государственное')
        PRIVATE = 'private', _('Частное')

    name            = models.CharField(max_length=255, verbose_name=_('Название'))
    slug            = models.SlugField(unique=True, verbose_name=_('Псевдоним'))
    description     = models.TextField(blank=True, verbose_name=_('Описание'))
    institution_type = models.CharField(
        max_length=20,
        choices=InstitutionType.choices,
        verbose_name=_('Тип учреждения')
    )
    ownership_type = models.CharField(
        max_length=20,
        choices=OwnershipType.choices,
        verbose_name=_('Форма собственности')
    )
    region          = models.CharField(max_length=100, verbose_name=_('Регион'))
    address         = models.CharField(max_length=255, verbose_name=_('Адрес'))
    phone           = models.CharField(max_length=20, verbose_name=_('Телефон'))
    email           = models.EmailField(blank=True, verbose_name=_('Email'))
    latitude        = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name=_('Широта')
    )
    longitude       = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name=_('Долгота')
    )
    logo            = models.ImageField(
        upload_to='institutions/logos/', blank=True, null=True, verbose_name=_('Логотип')
    )
    is_top          = models.BooleanField(default=False, verbose_name=_('ТОП учреждение'))
    is_active       = models.BooleanField(default=False, verbose_name=_('Проверено и активно'))
    created_at      = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at      = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        verbose_name = _('Учреждение')
        verbose_name_plural = _('Учреждения')
        ordering = ['-is_top', 'name']

    def __str__(self):
        return self.name


class Department(models.Model):
    institution   = models.ForeignKey(
        Institution,
        related_name='departments',
        on_delete=models.CASCADE,
        verbose_name=_('Учреждение')
    )
    name           = models.CharField(max_length=255, verbose_name=_('Отделение'))
    description    = models.TextField(blank=True, verbose_name=_('Описание'))
    created_at     = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at     = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        unique_together = ('institution', 'name')
        verbose_name = _('Отделение')
        verbose_name_plural = _('Отделения')

    def __str__(self):
        return f"{self.institution.name} — {self.name}"

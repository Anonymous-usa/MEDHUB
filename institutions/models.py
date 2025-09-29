from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, SoftDeleteModel, City
from core.utils import generate_unique_slug


class Institution(TimeStampedModel, SoftDeleteModel):
    """
    Медицинское учреждение (больница, клиника, лаборатория и т.д.)
    """

    class InstitutionType(models.TextChoices):
        HOSPITAL = 'hospital', _('Больница')
        CLINIC = 'clinic', _('Клиника')
        LABORATORY = 'laboratory', _('Лаборатория')
        OTHER = 'other', _('Другое')

    class OwnershipType(models.TextChoices):
        STATE = 'state', _('Государственное')
        PRIVATE = 'private', _('Частное')

    name = models.CharField(max_length=255, verbose_name=_('Название'))
    slug = models.SlugField(unique=True, verbose_name=_('Псевдоним'))
    description = models.TextField(blank=True, verbose_name=_('Описание'))

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

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Город'),
        related_name='institutions'
    )

    address = models.CharField(max_length=255, verbose_name=_('Адрес'))
    phone = models.CharField(max_length=20, verbose_name=_('Телефон'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name=_('Широта')
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name=_('Долгота')
    )

    logo = models.ImageField(
        upload_to='institutions/logos/', blank=True, null=True, verbose_name=_('Логотип')
    )

    is_top = models.BooleanField(default=False, verbose_name=_('ТОП учреждение'))

    class Meta:
        verbose_name = _('Учреждение')
        verbose_name_plural = _('Учреждения')
        ordering = ['-is_top', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
            models.Index(fields=['institution_type']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
        else:
            self.slug = generate_unique_slug(self, self.slug)
        super().save(*args, **kwargs)

    @property
    def region(self):
        """
        Возвращает регион, связанный с городом учреждения (если есть).
        """
        return getattr(self.city, "region", None)


class Department(TimeStampedModel, SoftDeleteModel):
    """
    Отделение внутри учреждения (например: кардиология, лаборатория).
    """
    institution = models.ForeignKey(
        Institution,
        related_name='departments',
        on_delete=models.CASCADE,
        verbose_name=_('Учреждение')
    )
    name = models.CharField(max_length=255, verbose_name=_('Отделение'))
    description = models.TextField(blank=True, verbose_name=_('Описание'))

    class Meta:
        unique_together = ('institution', 'name')
        verbose_name = _('Отделение')
        verbose_name_plural = _('Отделения')
        ordering = ['institution__name', 'name']
        indexes = [
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.institution.name} — {self.name}"

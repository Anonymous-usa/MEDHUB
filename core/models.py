from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeStampedModel(models.Model):
    """
    Абстрактная модель с датами создания и обновления.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Абстрактная модель с мягким удалением.
    """
    is_active  = models.BooleanField(default=True, verbose_name=_('Активно'))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Дата удаления'))

    class Meta:
        abstract = True


class Region(TimeStampedModel):
    """
    Справочник регионов Таджикистана.
    """
    name = models.CharField(max_length=100, verbose_name=_('Регион'))
    slug = models.SlugField(unique=True, verbose_name=_('Псевдоним'))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Регион')
        verbose_name_plural = _('Регионы')
        ordering = ['name']

    def __str__(self):
        return self.name


class City(TimeStampedModel):
    """
    Города, привязанные к региону.
    """
    region = models.ForeignKey(
        Region,
        related_name='cities',
        on_delete=models.CASCADE,
        verbose_name=_('Регион')
    )
    name = models.CharField(max_length=100, verbose_name=_('Город'))
    slug = models.SlugField(unique=True, verbose_name=_('Псевдоним'))

    class Meta:
        unique_together = ('region', 'name')
        verbose_name = _('Город')
        verbose_name_plural = _('Города')
        ordering = ['region__name', 'name']

    def __str__(self):
        return f"{self.name}, {self.region.name}"

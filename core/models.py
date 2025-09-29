from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """
    Абстрактная модель с датами создания и обновления.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class SoftDeleteModel(models.Model):
    """
    Абстрактная модель для мягкого удаления.
    """
    is_active = models.BooleanField(default=True, verbose_name=_('Активно'))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Дата удаления'))

    class Meta:
        abstract = True


class Region(TimeStampedModel, SoftDeleteModel):
    """
    Регион (например: Согдийская область, Хатлонская область).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Регион'))
    slug = models.SlugField(unique=True, verbose_name=_('Псевдоним'))

    class Meta:
        verbose_name = _('Регион')
        verbose_name_plural = _('Регионы')
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)


class City(TimeStampedModel, SoftDeleteModel):
    """
    Город, привязанный к региону.
    """
    region = models.ForeignKey(
        Region,
        related_name='cities',
        on_delete=models.CASCADE,
        verbose_name=_('Регион')
    )
    name = models.CharField(max_length=100, verbose_name=_('Город'))
    slug = models.SlugField(verbose_name=_('Псевдоним'))

    class Meta:
        unique_together = ('region', 'name')
        verbose_name = _('Город')
        verbose_name_plural = _('Города')
        ordering = ['region__name', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name}, {self.region.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)

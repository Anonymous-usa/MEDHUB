from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Region, City
from .utils import generate_unique_slug


@receiver(pre_save, sender=Region)
def set_region_slug(sender, instance, **kwargs):
    """
    Автоматически генерирует уникальный slug для региона перед сохранением.
    Если slug уже задан вручную — нормализует его.
    """
    if instance.name:
        if not instance.slug:
            instance.slug = generate_unique_slug(instance, instance.name)
        else:
            instance.slug = generate_unique_slug(instance, instance.slug)


@receiver(pre_save, sender=City)
def set_city_slug(sender, instance, **kwargs):
    """
    Автоматически генерирует уникальный slug для города перед сохранением.
    Если slug уже задан вручную — нормализует его.
    """
    if instance.name:
        if not instance.slug:
            instance.slug = generate_unique_slug(instance, instance.name)
        else:
            instance.slug = generate_unique_slug(instance, instance.slug)

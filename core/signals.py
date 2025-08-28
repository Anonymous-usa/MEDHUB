from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Region, City
from .utils import generate_unique_slug

@receiver(pre_save, sender=Region)
def set_region_slug(sender, instance, **kwargs):
    """
    Автоматически генерирует уникальный slug для региона перед сохранением.
    """
    if not instance.slug and instance.name:
        instance.slug = generate_unique_slug(instance, instance.name)


@receiver(pre_save, sender=City)
def set_city_slug(sender, instance, **kwargs):
    """
    Автоматически генерирует уникальный slug для города перед сохранением.
    """
    if not instance.slug and instance.name:
        instance.slug = generate_unique_slug(instance, instance.name)

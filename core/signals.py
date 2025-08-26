from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Region, City
from .utils import generate_unique_slug

@receiver(pre_save, sender=Region)
def set_region_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance, instance.name)

@receiver(pre_save, sender=City)
def set_city_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance, instance.name)

from django.contrib import admin
from .models import Region, City

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'slug', 'created_at')
    list_filter = ('region',)
    prepopulated_fields = {'slug': ('name',)}

from django.urls import path
from .views import RegionListView, CityListView

app_name = 'core'

urlpatterns = [
    # Публичный список регионов
    path('v1/regions/', RegionListView.as_view(), name='region-list'),

    # Список городов по региону
    path('v1/regions/<slug:region_slug>/cities/', CityListView.as_view(), name='city-list'),
]

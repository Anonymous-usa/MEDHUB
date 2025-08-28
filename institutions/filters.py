# institutions/filters.py
import django_filters
from .models import Institution
from accounts.models import Doctor  # Assuming Doctor model lives in accounts app


class InstitutionFilter(django_filters.FilterSet):
    """
    Фильтры для списка учреждений.
    - region: по ID региона через связь с городом
    - city: по ID города
    - institution_type: по типу учреждения
    - ownership_type: по форме собственности
    """
    region = django_filters.NumberFilter(field_name='city__region_id')
    city = django_filters.NumberFilter(field_name='city_id')
    institution_type = django_filters.CharFilter(field_name='institution_type')
    ownership_type = django_filters.CharFilter(field_name='ownership_type')

    class Meta:
        model = Institution
        fields = ['region', 'city', 'institution_type', 'ownership_type', 'is_top', 'is_active']


class DoctorFilter(django_filters.FilterSet):
    """
    Фильтры для списка врачей.
    - specialization: по специализации
    - institution: по ID учреждения
    - department: по ID отделения
    """
    specialization = django_filters.CharFilter(field_name='specialization')
    institution = django_filters.NumberFilter(field_name='institution_id')
    department = django_filters.NumberFilter(field_name='department_id')

    class Meta:
        model = Doctor
        fields = ['specialization', 'institution', 'department']

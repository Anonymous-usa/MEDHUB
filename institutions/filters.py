import django_filters
from .models import Institution
from accounts.models import Doctor  # Модель врача из accounts


class InstitutionFilter(django_filters.FilterSet):
    """
    Фильтры для списка учреждений.
    - region: по ID региона через связь с городом
    - city: по ID города
    - institution_type: по типу учреждения
    - ownership_type: по форме собственности
    - is_top: только ТОП учреждения
    - is_active: только активные
    """
    region = django_filters.NumberFilter(field_name='city__region_id')
    city = django_filters.NumberFilter(field_name='city_id')
    institution_type = django_filters.CharFilter(field_name='institution_type', lookup_expr='iexact')
    ownership_type = django_filters.CharFilter(field_name='ownership_type', lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Institution
        fields = [
            'region',
            'city',
            'institution_type',
            'ownership_type',
            'is_top',
            'is_active',
            'name',
        ]


class DoctorFilter(django_filters.FilterSet):
    """
    Фильтры для списка врачей.
    - specialization: по специализации (частичное совпадение)
    - institution: по ID учреждения
    - department: по ID отделения
    """
    specialization = django_filters.CharFilter(field_name='specialization', lookup_expr='icontains')
    institution = django_filters.NumberFilter(field_name='institution_id')
    department = django_filters.NumberFilter(field_name='department_id')
    full_name = django_filters.CharFilter(field_name='full_name', lookup_expr='icontains')

    class Meta:
        model = Doctor
        fields = ['specialization', 'institution', 'department', 'full_name']

import django_filters
from .models import Institution, Doctor

class InstitutionFilter(django_filters.FilterSet):
    region = django_filters.NumberFilter(field_name='region_id')
    type = django_filters.CharFilter(field_name='type')
    ownership = django_filters.CharFilter(field_name='ownership')

    class Meta:
        model = Institution
        fields = ['region', 'type', 'ownership']

class DoctorFilter(django_filters.FilterSet):
    specialization = django_filters.CharFilter(field_name='specialization')
    institution = django_filters.NumberFilter(field_name='institution_id')
    department = django_filters.NumberFilter(field_name='department_id')

    class Meta:
        model = Doctor
        fields = ['specialization', 'institution', 'department']
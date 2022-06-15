import django_filters
from .models import *
from django_filters import DateFilter, CharFilter


class QueryFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date', lookup_expr='gte')
    end_date = DateFilter(field_name='date', lookup_expr='lte')
    target = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Query
        fields = ['type', 'status']

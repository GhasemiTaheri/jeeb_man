from django_filters import NumberFilter
from django_filters.rest_framework import FilterSet, CharFilter

from management.models import Transaction


class TransactionFilterSet(FilterSet):
    from_date = NumberFilter(field_name='date', lookup_expr='gte')
    to_date = NumberFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['category', 'group']

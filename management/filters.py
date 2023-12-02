from django_filters.rest_framework import FilterSet, DateFilter

from management.models import Transaction


class TransactionFilterSet(FilterSet):
    from_date = DateFilter(field_name='date', lookup_expr='gte')
    to_date = DateFilter(field_name='date', lookup_expr='lt')

    class Meta:
        model = Transaction
        fields = ['category', 'group']

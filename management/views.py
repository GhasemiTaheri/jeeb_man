from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from management.filters import TransactionFilterSet
from management.models import Transaction
from management.serializers import TransactionSerializer, \
    CategoryExpenseSerializer


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilterSet

    def get_queryset(self):
        return Transaction.scoop_objects \
            .filter_by_user(self.request.user) \
            .select_related('owner').order_by('id')


class ReportViewSet(GenericViewSet):

    @action(detail=False)
    def get_balance(self, request, *args, **kwargs):
        spends = Transaction.objects \
            .filter(owenr=self.request.user, group='1') \
            .values('owner') \
            .aggregate(total_expense=Sum('amount')) \
            .values('total_expense')

        earns = Transaction.objects \
            .filter(owenr=self.request.user,
                    group='2') \
            .values('owner') \
            .aggregate(total_earn=Sum('amount')) \
            .values('total_earn')

        result = earns - spends

        return Response(data={'balance': result})

    @action(detail=False, serializer_class=CategoryExpenseSerializer)
    def category_expense(self, request, *args, **kwargs):
        queryset = Transaction.objects \
            .filter(owenr=self.request.user, group='1') \
            .values('category') \
            .annotate(expense=Sum('amount')) \
            .values('category', 'expense')

        serializer = self.get_serializer(instance=queryset, many=True)

        return Response(data=serializer.data)

    # todo: create a serializer for this report
    @action(detail=False, serializer_class=CategoryExpenseSerializer)
    def month_expense(self, request, *args, **kwargs):
        queryset = Transaction.objects \
            .filter(owner=self.request.user, group='1') \
            .annotate(month=TruncMonth('date')) \
            .values('month') \
            .annotate(expence=Sum('amount')) \
            .values('month', 'c')

        serializer = self.get_serializer(instance=queryset, many=True)

        return Response(data=serializer.data)

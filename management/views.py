from django.db.models import Sum, F
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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

    @action(detail=False)
    def get_balance(self, request, *args, **kwargs):
        queryset = Transaction.objects.filter(owner=self.request.user)

        spends = queryset.filter(group='1') \
            .values('owner') \
            .aggregate(total_expense=Sum('amount'))

        earns = queryset.filter(group='2') \
            .values('owner') \
            .aggregate(total_earn=Sum('amount'))

        result = (int(earns.get('total_earn', 0))
                  - int(spends.get('total_expense', 0)))

        return Response(data={'balance': result})

    @action(detail=False, serializer_class=CategoryExpenseSerializer)
    def category_expense(self, request, *args, **kwargs):
        queryset = Transaction.objects \
            .filter(owner=self.request.user, group='1') \
            .values('category', name=F('category__name')) \
            .annotate(expense=Sum('amount'))

        serializer = self.get_serializer(instance=queryset, many=True)

        return Response(data=serializer.data)

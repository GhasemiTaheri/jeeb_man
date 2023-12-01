from rest_framework.viewsets import ModelViewSet, GenericViewSet

from management.models import Transaction
from management.serializers import TransactionSerializer


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.scoop_objects \
            .filter_by_user(self.request.user) \
            .select_related('owner')


class ReportViewSet(GenericViewSet):
    pass
from django.db.models import QuerySet


class TransactionManager(QuerySet):
    """
    The methods of this class filter the rows of the Transaction table
    """

    def filter_by_user(self, user) -> QuerySet:
        return self.filter(owner=user)

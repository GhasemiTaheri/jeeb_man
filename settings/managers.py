from django.db.models import QuerySet


class CategoryManager(QuerySet):
    """
    The methods of this class filter the rows of the Category table
    """

    def public_category(self) -> QuerySet:
        return self.filter(owner__isnull=True)  # these are public category

    def filter_by_user(self, user) -> QuerySet:
        result = self.filter(owner=user)
        # append public category
        result |= self.public_category()

        return result

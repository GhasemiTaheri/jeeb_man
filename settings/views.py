from rest_framework.viewsets import ModelViewSet

from settings.models import Category
from settings.policy import CategoryAccessPolicy
from settings.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [CategoryAccessPolicy]

    def get_queryset(self):
        """
        User categories plus public categories
        """
        return Category.scoop_objects.filter_by_user(user=self.request.user) \
            .order_by('id')

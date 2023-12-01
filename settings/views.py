from rest_framework.viewsets import ModelViewSet

from settings.models import Category
from settings.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

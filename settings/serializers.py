from rest_framework import serializers
from rest_framework.fields import HiddenField, CurrentUserDefault

from settings.models import Category
from utility.drf.serializer_helper import DisplayTextChoicesField


class CategorySerializer(serializers.ModelSerializer):
    group = DisplayTextChoicesField(choices=Category.GROUP_TYPE)
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Category
        fields = '__all__'

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import HiddenField, CurrentUserDefault, IntegerField

from management.models import Transaction
from settings.models import Category
from utility.drf.serializer_helper import DisplayTextChoicesField, \
    PkSlugRelatedField


class TransactionSerializer(serializers.ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())
    group = DisplayTextChoicesField(choices=Transaction.GROUP_TYPE)
    category = PkSlugRelatedField(slug_field='name',
                                  queryset=Category.objects.all())

    class Meta:
        model = Transaction
        fields = '__all__'

    def validate_category(self, value):
        """
        Users can only choose general categories or
        categories they have created
        """
        current_user = self.context.get('request').user
        if value.owner is not None and value.owner != current_user:
            raise ValidationError('شما مجاز به انتخاب این دسته بندی نیستید')

        return value


class CategoryExpenseSerializer(serializers.Serializer):
    category = PkSlugRelatedField(slug_field='name',
                                  queryset=Category.objects.all())
    expense = IntegerField()

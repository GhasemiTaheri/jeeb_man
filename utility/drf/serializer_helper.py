from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from rest_framework import serializers
from rest_framework.fields import ChoiceField


class DisplayTextChoicesField(ChoiceField):
    """
    get value in to_internal_value and represent display test for client
    """

    def to_representation(self, value):
        if value in ('', None):
            return value
        return self.choices.get(value)


class PkSlugRelatedField(serializers.SlugRelatedField):
    """
        This class is used when we want to receive the id of an object as an
        input and display our desired field
    """

    def __init__(self, **kwargs):

        # select field in UI new text and Id for creating their options
        self.use_on_select = kwargs.pop('use_on_select_field', False)

        super().__init__(**kwargs)

    default_error_messages = {
        'does_not_exist': 'شی با id={value} وجود ندارد',
        'invalid': 'مقدار اشتباه است',
    }

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get(id=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field,
                      value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        if not self.use_on_select:
            return super().to_representation(obj)

        return {
            'id': getattr(obj, 'id'),
            'text': super().to_representation(obj)
        }

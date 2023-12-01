from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        return make_password(value)


class RegisterSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['username', 'password']


class MeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'phone_number']

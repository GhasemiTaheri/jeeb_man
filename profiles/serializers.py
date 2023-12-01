from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'read_only': True}
        }

    def validate_password(self, value):
        return make_password(value)


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number']
        read_only_fields = ('username', 'role')


class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['email', 'last_login', 'date_joined', 'groups',
                   'user_permissions', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        depth = 1

    def validate_password(self, value):
        return make_password(value)

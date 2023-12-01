from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from profiles.serializers import MeSerializer, UserManagementSerializer, \
    RegisterSerializer


class RegisterApiView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # anyone can send request


class MeView(RetrieveUpdateDestroyAPIView):
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.request.user)
        return Response(serializer.data)


class UserManagementViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserManagementSerializer
    permission_classes = []  # todo: this viewset is just for admin

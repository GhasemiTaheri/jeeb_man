from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from profiles.serializers import MeSerializer, RegisterSerializer


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

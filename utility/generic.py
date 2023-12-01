from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestHelperUtility(APITestCase):

    def create_user(self, **kwargs):
        return get_user_model().objects.create_user(**kwargs)

    def get_user_credentials(self, **kwargs):
        token_pair_request = self.client.post(
            reverse('token_obtain_pair'),
            kwargs)
        return f"Bearer {token_pair_request.data.get('access')}"

    def _check_response_by_property(self, data, key, value):
        for obj in data:
            self.assertEqual(obj[key], value)

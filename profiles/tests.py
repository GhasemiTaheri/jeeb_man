from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from profiles.models import User


class TestHelperUtility(APITestCase):

    def create_user(self, **kwargs):
        return User.objects.create_user(**kwargs)

    def get_user_credentials(self, **kwargs):
        token_pair_request = self.client.post(
            reverse('token_obtain_pair'),
            kwargs)
        return f"Bearer {token_pair_request.data.get('access')}"

    def _check_response_by_property(self, data, key, value):
        for obj in data:
            self.assertEqual(obj[key], value)


class RegisterTestCase(TestHelperUtility):

    def setUp(self) -> None:
        self.base_url = reverse('register_user')

    def test_register(self):
        response = self.client.post(self.base_url,
                                    data={'username': 'test',
                                          'password': 'test'})
        self.assertEqual(response.status_code, 201)

    def test_illegal_method(self):
        self.assertNotEqual(self.client.get(self.base_url).status_code, 200)
        self.assertNotEqual(self.client.delete(self.base_url).status_code, 200)
        self.assertNotEqual(self.client.put(self.base_url).status_code, 200)
        self.assertNotEqual(self.client.patch(self.base_url).status_code, 200)


class MeViewTestCase(TestHelperUtility):
    def setUp(self) -> None:
        self.base_url = reverse('me')
        self.u1 = self.create_user(username='u1',
                                   password="12345",
                                   phone_number='09112223344')

    def test_access_control(self):
        # test without credentials
        access_denied = self.client.get(self.base_url)
        self.assertNotEqual(access_denied.status_code, 200)

        # test with credentials
        u1_token = self.get_user_credentials(username='u1', password="12345")
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)
        with_access = self.client.get(self.base_url)
        self.assertEqual(with_access.status_code, 200)

        # clear credentials
        self.client.credentials()

    def test_see_me(self):
        u1_token = self.get_user_credentials(username='u1', password="12345")
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)

        get_request = self.client.get(self.base_url)
        self.assertEqual(get_request.data.get('id'), self.u1.id)

    def test_update_me(self):
        u1_token = self.get_user_credentials(username='u1', password="12345")
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)

        # healthy data
        patch_request = self.client.patch(self.base_url,
                                          {'first_name': 'test',
                                           'last_name': 'test last',
                                           'phone_number': '09122223344'})
        self.assertEqual(patch_request.status_code, 200)

        # bad data
        bad_request = self.client.patch(self.base_url,
                                        # send wrong data
                                        {'phone_number': '09122344'})
        self.assertEqual(bad_request.status_code, 400)

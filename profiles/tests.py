from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from profiles.models import User


class TestHelperUtility(APITestCase):

    def create_user(self, **kwargs):
        return User.objects.create_user(**kwargs)

    def get_user_credentials(self, **kwargs):
        token_pair_request = self.client.post(reverse('token_obtain_pair'),
                                              kwargs)
        return f"Bearer {token_pair_request.data.get('access')}"

    def _check_response_by_property(self, data, key, value):
        for obj in data:
            self.assertEqual(obj[key], value)


class RegisterTestCase(TestHelperUtility):

    def setUp(self) -> None:
        self.baseUrl = reverse('register_user')

    def test_register(self):
        response = self.client.post(self.baseUrl,
                                    data={'username': 'test',
                                          'password': 'test'})
        self.assertEqual(response.status_code, 201)

    def test_illegal_method(self):
        self.assertNotEqual(self.client.get(self.baseUrl).status_code, 200)
        self.assertNotEqual(self.client.delete(self.baseUrl).status_code, 200)
        self.assertNotEqual(self.client.put(self.baseUrl).status_code, 200)
        self.assertNotEqual(self.client.patch(self.baseUrl).status_code, 200)


class MeViewTestCase(TestHelperUtility):
    def setUp(self) -> None:
        self.baseUrl = reverse('me')
        self.u1 = self.create_user(username='u1', password="12345",
                                   phone_number='09112223344')

    def test_access_control(self):
        # test without credentials
        access_denied = self.client.get(self.baseUrl)
        self.assertNotEqual(access_denied.status_code, 200)

        # test with credentials
        u1_token = self.get_user_credentials(username='u1', password="12345")
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)
        with_access = self.client.get(self.baseUrl)
        self.assertEqual(with_access.status_code, 200)

        # clear credentials
        self.client.credentials()

    def test_see_me(self):
        u1_token = self.get_user_credentials(username='u1', password="12345")
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)

        get_request = self.client.get(self.baseUrl)
        self.assertEqual(get_request.data.get('id'), self.u1.id)

    def test_update_me(self):
        u1_token = self.get_user_credentials(username='u1', password="12345")
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)

        # healthy data
        patch_request = self.client.patch(self.baseUrl,
                                          {'first_name': 'test',
                                           'last_name': 'test last',
                                           'phone_number': '09122223344'})
        self.assertEqual(patch_request.status_code, 200)

        # bad data
        bad_request = self.client.patch(self.baseUrl,
                                        {'phone_number': '091222344'})
        self.assertEqual(bad_request.status_code, 400)


class UserManagementViewSetTestCase(TestHelperUtility):
    def setUp(self) -> None:
        # admin user
        self.u1 = self.create_user(username='u1', password="12345",
                                   phone_number='09112223344',
                                   is_superuser=True)
        # normal user
        for username in ['n1', 'n2', 'n3']:
            User.objects.create_user(username=username, password='12345')

    def test_admin_access_control(self):
        u1_token = self.get_user_credentials(username='u1', password="12345")
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)

        # list
        response = self.client.get(reverse('user_management-list'))
        self.assertEqual(response.status_code, 200)

        # select
        response = self.client.get(reverse('user_management-select'))
        self.assertEqual(response.status_code, 200)

        # create
        response = self.client.post(reverse('user_management-list'), data={
            'username': 'test2',
            'phone_number': '09123332211',
            'password': '1234567',
            'national_id': '1250570123',
            'province': '1',
        })
        self.assertEqual(response.status_code, 201)

        # update
        user_id = response.data.get('id')
        response = self.client.patch(
            reverse('user_management-detail', args=[user_id]), data={
                'first_name': 'foo'
            })
        self.assertEqual(response.status_code, 200)

        # detail
        response = self.client.get(
            reverse('user_management-detail', args=[user_id]))
        self.assertEqual(response.status_code, 200)

        # delete
        response = self.client.delete(
            reverse('user_management-detail', args=[user_id]))
        self.assertEqual(response.status_code, 204)
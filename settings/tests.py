from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from settings.models import Category
from utility.generic import TestHelperUtility


class CategoryTestCase(TestHelperUtility):
    def _add_category(self, name_list, group, owner=None):
        for i in name_list:
            Category.objects.create(name=i, group=group, owner=owner)

    def setUp(self) -> None:
        self.base_url = reverse('category-list')

        # add public expense category
        self._add_category(['trip', 'food', 'transport'], '1')
        # add public income category
        self._add_category(['salary', 'gift'], '2')

        # u1 categories
        self.u1 = get_user_model().objects.create_user(username='u1',
                                                       password='12345')
        self._add_category(['gym', 'coffee'], '1', self.u1)
        self._add_category(['sell', 'airdrop'], '2', self.u1)

        # u2 categories
        self.u2 = get_user_model().objects.create_user(username='u2',
                                                       password='12345')
        self._add_category(['closet', 'education'], '1', self.u2)
        self._add_category(['rent'], '2', self.u2)

        # u3 categories
        self.u3 = get_user_model().objects.create_user(username='u3',
                                                       password='12345')

    def test_default_category(self):
        """
        All users must have access to public categories
        """
        u3_token = self.get_user_credentials(username='u3', password='12345')
        self.client.credentials(HTTP_AUTHORIZATION=u3_token)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        for i in response.data.get('results'):
            self.assertEqual(Category.objects.get(id=i.get('id')).owner, None)

    def test_list(self):
        """
        Test list action
        """
        u1_token = self.get_user_credentials(username='u1', password='12345')
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        for i in response.data.get('results'):
            self.assertIn(Category.objects.get(id=i.get('id')).owner,
                          [self.u1, None])

    def test_create_category(self):
        """
        Test update action
        """
        u1_token = self.get_user_credentials(username='u1', password='12345')
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)

        response = self.client.post(self.base_url, data={
            'name': 'shoes',
            "group": '1',
            # try for create for another user THIS IS A ACCESS CHECK TOO
            'owner': self.u2.id
        })
        self.assertEqual(response.status_code, 201)

        # then we need check all category list
        self.test_list()

    def test_update_user_category(self):
        u1_token = self.get_user_credentials(username='u1', password='12345')
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)

        # healthy update
        category = Category.objects.filter(owner=self.u1).first()
        response = self.client.patch(reverse('category-detail', [category.id]),
                                     data={
                                         'name': 'Hiii',
                                         # try to change owner ship
                                         # 'owner': self.u2.id
                                     })
        self.assertEqual(response.status_code, 200)

        # update values
        category.refresh_from_db()
        self.assertEqual(category.name, 'Hiii')
        self.assertEqual(category.owner, self.u1)

        # try to update un access record
        category = Category.objects.filter(owner__isnull=True).first()
        response = self.client.patch(reverse('category-detail', [category.id]),
                                     data={
                                         'name': 'Hiii',
                                         # try to change owner ship
                                         'owner': self.u1.id
                                     })
        self.assertNotEqual(response.status_code, 200)
        # update values
        category.refresh_from_db()
        self.assertNotEqual(category.name, 'Hiii')
        self.assertNotEqual(category.owner, self.u1)

    def test_delete_category(self):
        u1_token = self.get_user_credentials(username='u1', password='12345')
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)

        # try to delete owen category
        category = Category.objects.filter(owner=self.u1).first()
        response = self.client.delete(
            reverse('category-detail', [category.id]))
        self.assertEqual(response.status_code, 204)

        # try to delete public
        category = Category.objects.filter(owner__isnull=True).first()
        response = self.client.patch(reverse('category-detail', [category.id]))
        self.assertNotIn(response.status_code, [200, 204])

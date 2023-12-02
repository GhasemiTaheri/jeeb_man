from rest_framework.reverse import reverse

from management.models import Transaction
from utility.generic import TestHelperUtility


class TransactionViewSetTestCase(TestHelperUtility):
    fixtures = ['test_data.json']

    def setUp(self) -> None:
        self.base_url = reverse('transaction-list')
        u1_token = self.get_user_credentials(username='user1',
                                             password='admin')
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)

    def test_list(self):
        u1_token = self.get_user_credentials(username='user1',
                                             password='admin')
        self.client.credentials(HTTP_AUTHORIZATION=u1_token)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        t1 = Transaction.objects.filter(owner__username='user1').first()
        response = self.client.patch(reverse('transaction-detail', [t1.id]),
                                     data={'amount': 25000})
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        t1 = Transaction.objects.filter(owner__username='user1').first()
        response = self.client.delete(reverse('transaction-detail', [t1.id]))
        self.assertEqual(response.status_code, 204)

    def test_get_balance(self):
        response = self.client.get(reverse('transaction-get-balance'))
        self.assertEqual(response.status_code, 200)

    def test_expense_by_category(self):
        response = self.client.get(reverse('transaction-category-expense'))
        self.assertEqual(response.status_code, 200)

    def test_monthly_expense(self):
        response = self.client.get(reverse('transaction-month-expense'))
        self.assertEqual(response.status_code, 200)

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from utility.generic import TestHelperUtility


class TransactionViewSetTestCase(TestHelperUtility):
    fixtures = ['test_data.json']

    def setUp(self) -> None:
        self.base_url = reverse('transaction-list')


    # def test_delete

from unittest import TestCase

from management.models import Transaction


class TransactionTestCase(TestCase):
    fixtures = ['test_data.json']

    def test_model(self):
        t1 = Transaction.objects.first()
        self.assertEqual(str(t1), t1.amount)
        self.assertTrue(hasattr(t1, 'owner'))
        self.assertTrue(hasattr(t1, 'amount'))
        self.assertTrue(hasattr(t1, 'group'))
        self.assertTrue(hasattr(t1, 'category'))
        self.assertTrue(hasattr(t1, 'date'))

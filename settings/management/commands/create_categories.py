from django.core.management import BaseCommand

from settings.models import Category


class Command(BaseCommand):

    def _create_expense_category(self):
        for i in ['food', 'trip', 'transport']:
            if not Category.objects.filter(name=i).exists():
                Category.objects.create(name=i, group='1', owner=None)

        print("expense category done")

    def _create_income_category(self):
        for i in ['salary', 'gift', 'sell']:
            if not Category.objects.filter(name=i).exists():
                Category.objects.create(name=i, group='2', owner=None)

        print("income category done")

    def handle(self, *args, **options):
        self._create_expense_category()
        self._create_income_category()

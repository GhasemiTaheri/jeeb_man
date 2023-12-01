from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from management.managers import TransactionManager


class Transaction(models.Model):
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              related_name='transactions',
                              verbose_name='مالک')
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                         verbose_name='مبلغ')
    GROUP_TYPE = [
        ('1', 'expense'),
        ('2', 'income')
    ]
    group = models.CharField(max_length=1, choices=GROUP_TYPE, null=True,
                             verbose_name='نوع تراکنش')
    category = models.ForeignKey('settings.Category',
                                 on_delete=models.PROTECT,
                                 related_name='transactions',
                                 verbose_name='دسته بندی')
    date = models.DateField(verbose_name='تاریخ')

    # model managers
    objects = models.Manager()
    scoop_objects = TransactionManager.as_manager()

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش ها'
        default_manager_name = 'objects'

    def __str__(self):
        return f'{self.amount}'

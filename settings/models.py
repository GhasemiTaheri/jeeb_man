from django.contrib.auth import get_user_model
from django.db import models

from settings.managers import CategoryManager


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='دسته بندی')
    GROUP_TYPE = [
        ('1', 'expense'),
        ('2', 'income')
    ]
    group = models.CharField(max_length=1, choices=GROUP_TYPE, default='1',
                             verbose_name='نوع دسته بندی')
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              related_name='categories',
                              # Only active users can create categories for
                              # themselves
                              limit_choices_to={'is_active': True},
                              # Categories that do not have an owner are
                              # considered public categories
                              null=True,
                              verbose_name='مالک')

    # model managers
    objects = models.Manager()
    scoop_objects = CategoryManager.as_manager()

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return f"{self.name}"

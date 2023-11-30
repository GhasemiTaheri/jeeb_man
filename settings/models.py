from django.contrib.auth import get_user_model
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='دسته بندی')
    GROUP_TYPE = [
        ('1', 'خرج'),
        ('2', 'درآمد')
    ]
    group = models.CharField(max_length=1, choices=GROUP_TYPE, default='1',
                             verbose_name='نوع دسته بندی')
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              related_name='categories',
                              # Only active users can create categories for
                              # themselves
                              limit_choices_to={'is_active': True},
                              null=True,
                              verbose_name='مالک')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return f"{self.name}"

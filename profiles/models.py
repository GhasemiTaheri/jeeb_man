from django.contrib.auth.models import AbstractUser
from django.db import models

from utility.db.validators import mobile_validator


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, null=True, blank=True,
                                    validators=[mobile_validator],
                                    verbose_name='شماره موبایل')

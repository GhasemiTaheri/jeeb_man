from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import os

username = os.getenv('ADMINISTRATOR_USERNAME', 'superuser')
password = os.getenv('ADMINISTRATOR_PASSWORD', 'superuser')
email = os.getenv('ADMINISTRATOR_EMAIL', 'superuser@example.com')

get_user_model().objects.get_or_create(
    username=username,
    defaults=dict(
        email=email,
        password=make_password(password),
        is_superuser=True,
        is_staff=True
    )
)



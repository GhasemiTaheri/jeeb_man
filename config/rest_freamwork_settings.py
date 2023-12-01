import datetime
import os


def build_django_rest_framework(custom_settings=None):
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'ACCESS_TOKEN_LIFETIME': datetime.timedelta(
            days=int(os.getenv('ACCESS_TOKEN_DAYS', '10')),
            minutes=int(os.getenv('ACCESS_TOKEN_MINUTES', '60')),
            seconds=int(os.getenv('ACCESS_TOKEN_SECONDS', '0')),
        ),
        'REFRESH_TOKEN_LIFETIME': datetime.timedelta(
            days=int(os.getenv('REFRESH_TOKEN_DAYS', '12')),
        ),
        'DEFAULT_PAGINATION_CLASS':
            'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 20,
    }
    if custom_settings:
        REST_FRAMEWORK.update(custom_settings)

    return REST_FRAMEWORK

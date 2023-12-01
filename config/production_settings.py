from .base_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASS'),
        'HOST': os.getenv('PRODUCTION_PG_HOST'),  # set in docker-compose
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

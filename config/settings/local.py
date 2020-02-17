from .base import *

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",  # 'django.db.backends.postgresql_psycopg2',
        "NAME": env.str("DJANGO_POSTGRES_DATABASE"),
        "USER": env.str("DJANGO_POSTGRES_USER"),
        "PASSWORD": env.str("DJANGO_POSTGRES_PASSWORD"),
        "HOST": env.str("DJANGO_POSTGRES_HOST"),
        "PORT": env.str("DJANGO_POSTGRES_PORT"),
    }
}

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
RESTRICT_ADMIN = False
DEBUG = True

# Secure cookie settings.
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False

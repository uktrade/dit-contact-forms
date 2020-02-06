from .base import *

import sys

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]["OPTIONS"]["debug"] = True  # noqa F405
TEMPLATES[0]["APP_DIRS"]: False
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",  # 'django.db.backends.postgresql_psycopg2',
        "NAME": os.environ.get("DJANGO_POSTGRES_DATABASE"),
        "USER": os.environ.get("DJANGO_POSTGRES_USER"),
        "PASSWORD": os.environ.get("DJANGO_POSTGRES_PASSWORD"),
        "HOST": os.environ.get("DJANGO_POSTGRES_HOST"),
        "PORT": os.environ.get("DJANGO_POSTGRES_PORT"),
    }
}

DEBUG = True
RESTRICT_ADMIN = False

# Secure cookie settings.
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False

STATIC_ROOT = "contact_form/static"
INTERNAL_IPS = ["127.0.0.1", "0.0.0.0", "localhost"]

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar}

ES_URL = "http://es:9200"

ELASTICSEARCH_DSL = {"default": {"hosts": ES_URL}}

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR + "/app-messages"

FEEDBACK_DESTINATION_EMAIL = os.environ.get("FEEDBACK_DESTINATION_EMAIL")

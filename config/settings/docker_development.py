from .base import *

DEBUG = True

# Secure cookie settings.
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False

STATIC_ROOT = "contact_forms/static"
INTERNAL_IPS = ["127.0.0.1", "0.0.0.0", "localhost"]

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar}

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR + "/app-messages"

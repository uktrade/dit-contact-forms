from .base import *

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
DEBUG = True

# Secure cookie settings.
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False

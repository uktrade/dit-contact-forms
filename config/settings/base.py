"""
Django settings for dit_helpdesk project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import logging
import os

from os.path import join as join_path

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.utils.log import DEFAULT_LOGGING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APPS_DIR = os.path.join(BASE_DIR, "contact_forms")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "a-secret-key")

ADMIN_ENABLED = os.environ.get("ADMIN_ENABLED", False)

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "raven.contrib.django.raven_compat",
    "formtools",
    "core",
    "cookies",
    "countries",
    "contact",
    "index",
    "django_extensions",
    "authbroker_client",
    "user",
    "healthcheck",
    "privacy_terms_and_conditions",
    "directory_forms_api_client",
    "accessibility",
    "disclaimer",
]

MIDDLEWARE = [
    "healthcheck.middleware.HealthCheckMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.AdminIpRestrictionMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": False,
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {"default": dj_database_url.config()}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 85000  # default is 1000

CACHES = {
    "default": {"BACKEND": "redis_cache.RedisCache", "LOCATION": "localhost:6379"}
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "authbroker_client.backends.AuthbrokerBackend",
]

FIXTURE_DIRS = ("countries/fixtures/",)

# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# SESSION_COOKIE_AGE = 5 * 60


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


STATIC_URL = "/assets/"
STATICFILES_DIRS = [join_path(APPS_DIR, "static_collected")]

STATIC_ROOT = join_path(
    APPS_DIR, "static"
)  # manage.py collectstatic will copy static files here

MEDIA_ROOT = join_path(APPS_DIR, "media")
MEDIA_URL = "/files/"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedStaticFilesStorage"
)  # compression without caching

# The correct index of the client IP in the X-Forwarded-For header.  It should be set to
# -2 if accessing the private domain and -3 if accessing the site via the public URL.
IP_SAFELIST_XFF_INDEX = int(os.environ.get("IP_SAFELIST_XFF_INDEX", "-2"))


RESTRICT_ADMIN = os.environ.get("RESTRICT_ADMIN", "True") == "True"
ALLOWED_ADMIN_IPS = os.environ.get("ALLOWED_ADMIN_IPS", "127.0.0.1").split(",")
ALLOWED_ADMIN_IP_RANGES = os.environ.get(
    "ALLOWED_ADMIN_IP_RANGES", "127.0.0.1/32"
).split(",")

# authbroker config
AUTHBROKER_URL = os.environ.get("AUTHBROKER_URL", "")
AUTHBROKER_CLIENT_ID = os.environ.get("AUTHBROKER_CLIENT_ID", "")
AUTHBROKER_CLIENT_SECRET = os.environ.get("AUTHBROKER_CLIENT_SECRET", "")

LOGIN_URL = os.environ.get("LOGIN_URL")

LOGIN_REDIRECT_URL = os.environ.get("LOGIN_REDIRECT_URL")

AUTH_USER_MODEL = "user.User"

FEEDBACK_MAX_LENGTH = 1000
CONTACT_MAX_LENGTH = 1000

# Secure cookie settings.
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SECURE = True

#os.environ.get("SENTRY_DSN")

LOGGING_CONFIG = None

LOGLEVEL = os.environ.get("LOGLEVEL", "info").upper()

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                # exact format is not important, this is the minimum information
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
            },
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            # console logs to stderr
            "console": {"class": "logging.StreamHandler", "formatter": "default"},
            # Add Handler for Sentry for `warning` and above
            "sentry": {
                "level": "WARNING",
                "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            # default for all undefined Python modules
            "": {"level": "WARNING", "handlers": ["console", "sentry"]},
            # Our application code
            "app": {
                "level": LOGLEVEL,
                "handlers": ["console", "sentry"],
                # Avoid double logging because of root logger
                "propagate": False,
            },
            # Prevent noisy modules from logging to Sentry
            "noisy_module": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": False,
            },
            # Default runserver request logging
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        },
    }
)

DIRECTORY_FORMS_API_BASE_URL = os.environ.get("DIRECTORY_FORMS_API_BASE_URL")
DIRECTORY_FORMS_API_API_KEY = os.environ.get("DIRECTORY_FORMS_API_API_KEY")
DIRECTORY_FORMS_API_SENDER_ID = os.environ.get("DIRECTORY_FORMS_API_SENDER_ID")
DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS = os.environ.get(
    "DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS", 0
)
DIRECTORY_CLIENT_CORE_CACHE_LOG_THROTTLING_SECONDS = os.environ.get(
    "DIRECTORY_CLIENT_CORE_CACHE_LOG_THROTTLING_SECONDS", 0
)
DIRECTORY_FORMS_API_DEFAULT_TIMEOUT = 10

APP_START_DOMAIN = os.environ.get("APP_START_DOMAIN")
FEEDBACK_DESTINATION_EMAIL = os.environ.get("FEEDBACK_DESTINATION_EMAIL")

HMRC_TAX_FORM_URL = os.environ.get("HMRC_TAX_FORM_URL")

IEE_GA_GTM = os.environ.get('IEE_GA_GTM')

EU_EXIT_DIT_EMAIL = os.environ.get("EU_EXIT_DIT_EMAIL")
EU_EXIT_DIT_FULLNAME = os.environ.get("EU_EXIT_DIT_FULLNAME")

EU_EXIT_EMAIL = os.environ.get("EU_EXIT_EMAIL")
EU_EXIT_FULLNAME = os.environ.get("EU_EXIT_FULLNAME")

FEEDBACK_EMAIL = os.environ.get("FEEDBACK_EMAIL")
FEEDBACK_FULLNAME = os.environ.get("FEEDBACK_FULLNAME")

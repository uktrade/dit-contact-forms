"""
With these settings, tests run faster.
"""
import logging.config
import os
import re

from django.conf import settings

DEBUG = False
from django.utils.log import DEFAULT_LOGGING

from .base import *

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")
# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    default="0GU5hi1N7kOZ3jcKZbVrk1CXX9MAnLOiuDyEyqIvAej2Tj7KlrA3Ey7jGgeW3NVd",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
# TEST_RUNNER = "django.test.runner.DiscoverRunner"
#
# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

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

INSTALLED_APPS.append("django_nose")
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
TEST_OUTPUT_DIR = os.environ.get("TEST_OUTPUT_DIR", ".")
NOSE_ARGS = [
    "--verbosity=3",
    "--nologcapture",
    "--with-spec",
    "--spec-color",
    "--with-xunit",
    "--xunit-file=%s/unittests.xml" % TEST_OUTPUT_DIR,
]

# Disable Django's logging setup
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

# Test Data

TEST_COUNTRY_CODE = "AU"
TEST_COUNTRY_NAME = "Australia"
COUNTRIES_DATA = APPS_DIR + "/countries/fixtures/countries_data.json"
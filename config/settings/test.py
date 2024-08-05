from .base import *

# import sys
#
## TEMPLATES
## ------------------------------------------------------------------------------
## https://docs.djangoproject.com/en/dev/ref/settings/#templates
# TEMPLATES[0]["OPTIONS"]["debug"] = True  # noqa F405
# TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa F405
#    (
#        "django.template.loaders.cached.Loader",
#        [
#            "django.template.loaders.filesystem.Loader",
#            "django.template.loaders.app_directories.Loader",
#        ],
#    )
# ]
#
# DEBUG = True
#
## Secure cookie settings.
# SESSION_COOKIE_SECURE = False
# SESSION_COOKIE_HTTPONLY = False
# CSRF_COOKIE_SECURE = False
#
# STATIC_ROOT = "contact_forms/static"
#
# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = BASE_DIR + "/app-messages"

# INSTALLED_APPS.append("django_nose")
# TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
# TEST_OUTPUT_DIR = env.str("TEST_OUTPUT_DIR")
# NOSE_ARGS = [
#    "--verbosity=3",
#    "--nologcapture",
#    "--with-spec",
#    "--spec-color",
#    "--with-xunit",
#    "--xunit-file=%s/unittests.xml" % TEST_OUTPUT_DIR,
# ]

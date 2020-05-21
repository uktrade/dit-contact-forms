from .base import *
import json


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


default_vcap = """{
    "redis": [
        {
            "credentials": {
                "uri": "redis://localhost"
            }
        }
    ]
}"""
VCAP_SERVICES = json.loads(env.str("VCAP_SERVICES", default_vcap))

REDIS_URL = VCAP_SERVICES["redis"][0]["credentials"]["uri"]

CACHES = {
    "default": {"BACKEND": "django_redis.cache.RedisCache", "LOCATION": REDIS_URL}
}

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar}

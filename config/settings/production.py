from .base import *
import json

assert not ADMIN_ENABLED and os.environ.get("DJANGO_SETTINGS_MODULE") == 'config.settings.production'

VCAP_SERVICES = json.loads(env.str("VCAP_SERVICES"))

REDIS_URL = VCAP_SERVICES["redis"][0]["credentials"]["uri"]

CACHES = {
    "default": {"BACKEND": "django_redis.cache.RedisCache", "LOCATION": REDIS_URL}
}

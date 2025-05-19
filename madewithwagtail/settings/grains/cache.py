from madewithwagtail.settings import ENVIRONMENT, PROJECT  # , CACHE_URL


__all__ = [
    "CACHES",
]  # don't import DEV_CACHES by default

# Dont use redis because we don't need it
# CACHES = {"default": django_cache_url.parse(CACHE_URL)}
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
    }
}

# Tests can't use manage.py createcachetable due to temporary database, so use dummy
DEV_CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Add a prefix to distinguish huey entries and app entries
CACHES.get("default").update({"PREFIX": "-".join([PROJECT, ENVIRONMENT])})

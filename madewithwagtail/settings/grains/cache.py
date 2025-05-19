from madewithwagtail.settings import ENVIRONMENT, PROJECT  # , CACHE_URL
from typed_environment_configuration import StringVariable

AWS_CONTENT_DISTRIBUTION_ID = StringVariable("AWS_CONTENT_DISTRIBUTION_ID").getenv()

__all__ = [
    "CACHES",
    "CACHALOT_TIMEOUT",
    "WAGTAILFRONTENDCACHE",
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

# When this isn't set, it will eventually fill up redis
CACHALOT_TIMEOUT = 300

# For frontend cache module
WAGTAILFRONTENDCACHE = {
    "cloudfront": {
        "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudfrontBackend",
        "DISTRIBUTION_ID": AWS_CONTENT_DISTRIBUTION_ID,
    }
}

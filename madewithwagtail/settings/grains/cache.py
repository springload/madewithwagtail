import django_cache_url

from madewithwagtail.settings import PROJECT, ENVIRONMENT #, CACHE_URL

__all__ = ["CACHES", "CACHALOT_TIMEOUT", "WAGTAILFRONTENDCACHE"]  # don't import DEV_CACHES by default

#Dont use redis because we don't need it
#CACHES = {"default": django_cache_url.parse(CACHE_URL)}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

#Tests can't use manage.py createcachetable due to temporary database, so use dummy
DEV_CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
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
        "DISTRIBUTION_ID": {
            #TODO change this when do the DNS changeover to madewithwagtail.org
            "madewithwagtail-preview-media.s3-website-ap-southeast-2.amazonaws.com": "E19LUSH371PZQA",
        },
    }
}

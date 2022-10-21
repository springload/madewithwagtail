from .base import *
from .grains.cache import *
from .grains.cache import DEV_CACHES
from .grains.logging import DEV_LOGGING

# Tests can't use manage.py createcachetable due to temporary database, so use dummy
CACHES = DEV_CACHES.copy()

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            normpath(join(DJANGO_ROOT, "core/templates")),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": True,
            "context_processors": ["django.template.context_processors.debug"]
            + CONTEXT_PROCESSORS,
        },
    },
]


# Analytics stuff
GOOGLE_TAG_MANAGER = False
GOOGLE_ANALYTICS_KEY = False
GOOGLE_MAPS_API_KEY = False

DEBUG = True

# To have fake email backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# As required by debug_toolbar
INTERNAL_IPS = (
    "10.0.2.2",
    "127.0.0.1",
)

INSTALLED_APPS += ("wagtail.contrib.styleguide",)

LOGGING = DEV_LOGGING.copy()

ALLOWED_HOSTS = ["*"]

CACHE_MIDDLEWARE_SECONDS = 0
# Change these if you want to enable recaptcha on submissions form
# https://github.com/springload/wagtail-django-recaptcha
RECAPTCHA_PUBLIC_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""
NOCAPTCHA = False


# NOTE: Enable with caution. DJDT will cause stack overflows
# on a lot of pages (anything using STD_STREAMFIELD, for example)

# INSTALLED_APPS += (
#     'django_extensions',
#     'debug_toolbar',
# )
# MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )

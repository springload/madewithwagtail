from .base import *

# Analytics stuff
GOOGLE_TAG_MANAGER = False
GOOGLE_ANALYTICS_KEY = False

DEBUG = True
TEMPLATE_DEBUG = True

COMPRESS_ENABLED = False

DATABASES['default']['PASSWORD'] = ''

# To have fake email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# As required by debug_toolbar
INTERNAL_IPS = (
   '10.0.2.2',
   '127.0.0.1',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

CACHE_MIDDLEWARE_SECONDS = 0

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE_CLASSES

from .base import *

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            normpath(join(DJANGO_ROOT, 'core/templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': ['django.template.context_processors.debug'] + CONTEXT_PROCESSORS
        }
    },
]

# Analytics stuff
GOOGLE_TAG_MANAGER = False
GOOGLE_ANALYTICS_KEY = False

DEBUG = True

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
    'wagtail.contrib.wagtailstyleguide',
)

CACHE_MIDDLEWARE_SECONDS = 0

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE_CLASSES

# Change these if you want to enable recaptcha on submissions form
# https://github.com/springload/wagtail-django-recaptcha
RECAPTCHA_PUBLIC_KEY = False
RECAPTCHA_PRIVATE_KEY = False
NOCAPTCHA = False

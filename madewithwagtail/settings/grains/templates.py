from os.path import normpath, join
from .paths import *

# Template configuration
CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.template.context_processors.request',
    'core.context_processors.baseurl',
    'core.context_processors.google_credentials',
    'core.context_processors.api_companies_endpoint',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            normpath(join(DJANGO_ROOT, 'core/templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': False,
            'context_processors': ['django.template.context_processors.debug'] + CONTEXT_PROCESSORS
        }
    },
]

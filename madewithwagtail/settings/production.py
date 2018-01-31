from .base import *
import os
import raven


RAVEN_CONFIG = {
    'dsn': 'https://d217d252fc444568afe6b639d1cbda28:62b3d23d132442dbab3886706e458f7c@sentry.io/255231',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(DJANGO_ROOT),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            normpath(join(DJANGO_ROOT, 'core/templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': False,
            'context_processors': CONTEXT_PROCESSORS
        }
    },
]
INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Makes session cookie work over HTTPS only
SESSION_COOKIE_SECURE = True


# Compress static files offline
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE

COMPRESS_OFFLINE = False
COMPRESS_ENABLED = True

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

# Static folder ready for production mode
STATIC_ROOT = join(DJANGO_ROOT, 'static')
STATICFILES_DIRS = ()

# Enables error emails.
CELERY_SEND_TASK_ERROR_EMAILS = True

BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = 'redis://'


#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# Use Redis as the cache backend for extra performance

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'KEY_PREFIX': SITE_NAME,
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        }
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
) + MIDDLEWARE_CLASSES + (
    'django.middleware.cache.FetchFromCacheMiddleware',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': join(DJANGO_ROOT, 'logs/%s.log' % SITE_NAME),
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 50,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'propagate': True,
            'level': 'ERROR',
        },
        'core': {
            'handlers': ['file', 'mail_admins'],
            'propagate': True,
            'level': 'ERROR',
        }
    }
}

try:
    from .local import *
except ImportError:
    pass

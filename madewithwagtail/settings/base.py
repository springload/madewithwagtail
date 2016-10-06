"""
Django settings for  project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os
from os.path import abspath, basename, dirname, join, normpath
from sys import path

# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(dirname(abspath(__file__))))

# Absolute filesystem path to the top-level project folder:
PROJECT_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

WAGTAIL_SITE_NAME = "Made with Wagtail"

# Search results template
WAGTAILSEARCH_RESULTS_TEMPLATE = 'core/search_results.html'

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)

"""
Two things are wrong with Django's default `SECRET_KEY` system:

1. It is not random but pseudo-random
2. It saves and displays the SECRET_KEY in `settings.py`

This snippet
1. uses `SystemRandom()` instead to generate a random key
2. saves a local `secret.txt`

The result is a random and safely hidden `SECRET_KEY`.
"""
try:
    SECRET_KEY
except NameError:
    SECRET_FILE = os.path.join(PROJECT_ROOT, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            import random
            SECRET_KEY = ''.join(
                [random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)]
            )
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            Exception('Please create a %s file with random characters to generate your secret key!' % SECRET_FILE)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'taggit',
    'modelcluster',
    'captcha',
    'wagtailcaptcha',
    'core',
    'overextends',
    'api',
    'wagtailgmaps',
    'rest_framework',
    'wagtail.contrib.wagtailsitemaps',
    'wagtail.contrib.wagtailroutablepage',
    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailsites',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',

    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

# Name and email addresses of recipients
ADMINS = (
    ('Tech-urgent', 'tech-urgent@springload.co.nz'),
)

# Default from address for CMS auto email messages (logs, errors..)
SERVER_EMAIL = 'errors@madewithwagtail.org'

# Default from address for CMS email messages to users (forgot password etc..)
DEFAULT_FROM_EMAIL = '%s@madewithwagtail.org' % SITE_NAME

ROOT_URLCONF = SITE_NAME + '.urls'
WSGI_APPLICATION = SITE_NAME + '.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'madewithwagtail',
        'USER': 'postgres',
        'HOST': '',  # Set to empty string for localhost.
        'PORT': '',  # Set to empty string for default.
        'CONN_MAX_AGE': 600,  # number of seconds database connections should persist for
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Pacific/Auckland'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATE_FORMAT = 'j F Y'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = (
    join(DJANGO_ROOT, 'static'),
)

MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Django compressor settings
# http://django-compressor.readthedocs.org/en/latest/settings/

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# Template configuration
CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'core.context_processors.baseurl',
    'core.context_processors.google_analytics',
    'core.context_processors.api_companies_endpoint',
    'django.contrib.messages.context_processors.messages',
]

# Wagtail settings

LOGIN_URL = 'wagtailadmin_login'
LOGIN_REDIRECT_URL = 'wagtailadmin_home'

# Wagtailgmaps settings

WAGTAIL_ADDRESS_MAP_CENTER = 'Wellington, New Zealand'
WAGTAIL_ADDRESS_MAP_ZOOM = 8

# REST framework

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
    'PAGINATE_BY': None,
}

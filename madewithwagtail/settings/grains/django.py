from madewithwagtail.settings import *
from .paths import *

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

ALLOWED_HOSTS = ADDRESSES  # set by env vars

# Application definition
SITE_ID = 1

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'taggit',
    'modelcluster',
    'captcha',
    'wagtailcaptcha',
    'core',
    'api',
    'wagtailgmaps',
    'rest_framework',
    'wagtail.contrib.postgres_search',
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

ROOT_URLCONF = SITE_NAME + '.urls'
WSGI_APPLICATION = SITE_NAME + '.wsgi.application'

#
TAGGIT_CASE_INSENSITIVE = True

if not DEBUG:
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS



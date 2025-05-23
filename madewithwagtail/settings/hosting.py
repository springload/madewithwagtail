from .base import *
from .grains.aws import *
from .grains.cache import *
from .grains.logging import LOGGING
from .grains.sentry import *

from typed_environment_configuration import StringVariable

AWS_CONTENT_DISTRIBUTION_ID = StringVariable(
    "AWS_CONTENT_DISTRIBUTION_ID", default=""
).getenv()

# Google Analytics settings
GOOGLE_TAG_MANAGER = False

DEBUG = False

STATICFILES_DIRS = ()

MIDDLEWARE = (
    (
        "django.middleware.common.BrokenLinkEmailsMiddleware",
        "django.middleware.cache.UpdateCacheMiddleware",
    )
    + MIDDLEWARE
    + ("django.middleware.cache.FetchFromCacheMiddleware",)
)

# Makes session cookie work over HTTPS only
SESSION_COOKIE_SECURE = True

SERVER_EMAIL = "errors@madewithwagtail.org"

# Tasks
TASKS_MAX_HOURS_RETRY = 72
TASKS_MAX_RETRIES = 12 * TASKS_MAX_HOURS_RETRY  # Keep trying in the next 72 hours
TASKS_RETRY_DELAY = 5 * 60  # 5 minutes delay


CACHE_MIDDLEWARE_SECONDS = 600
CACHE_TEMPLATE_FRAGMENTS_SECONDS = 600

# Make sure we include the needed Middleware apps
# Excluding logged in (admin) requests
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

SECURE_HSTS_SECONDS = 31536000

# For frontend cache module
WAGTAILFRONTENDCACHE = {
    "cloudfront": {
        "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudfrontBackend",
        "DISTRIBUTION_ID": AWS_CONTENT_DISTRIBUTION_ID,
    }
}

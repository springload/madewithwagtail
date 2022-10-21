import os

from .dev import *

os.environ["REUSE_DB"] = "1"

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

DEBUG = False
TEMPLATE_DEBUG = False

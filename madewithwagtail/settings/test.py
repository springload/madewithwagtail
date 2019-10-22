from .dev import *
import os

os.environ["REUSE_DB"] = "1"

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

DEBUG = False
TEMPLATE_DEBUG = False

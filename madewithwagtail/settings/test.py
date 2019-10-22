from .dev import *
import os

os.environ["REUSE_DB"] = "1"

TEST_RUNNER = "core.tests.utils.FastTestRunner"

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

DEBUG = False
TEMPLATE_DEBUG = False

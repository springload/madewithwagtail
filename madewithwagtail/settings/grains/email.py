from .. import PROJECT
from .django import SITE_NAME

EMAIL_BACKEND = "django_amazon_ses.EmailBackend"

AWS_SES_REGION = "ap-southeast-2"

# Only for task failure notifications
EXCEPTION_EMAIL_RECIPIENTS = ["tech-urgent@springload.co.nz"]

# Default from address for CMS auto email messages (logs, errors..)
SERVER_EMAIL = "errors@madewithwagtail.org"

# Default from address for CMS email messages to users (forgot password etc..)
DEFAULT_FROM_EMAIL = "%s@madewithwagtail.org" % SITE_NAME

import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from madewithwagtail.settings import APPLICATION_VERSION, ENVIRONMENT, PROJECT

from .. import *

SENTRY_RELEASE = APPLICATION_VERSION
SENTRY_ENVIRONMENT = ENVIRONMENT
_ENVVARS = [
    StringVariable("SENTRY_DSN_BED", default=""),
    StringVariable("SENTRY_DSN_FED", default=""),
    StringVariable("SENTRY_CSP_URL", default=""),
]

fill(_ENVVARS, vars(), prefix="")


sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)

sentry_sdk.init(
    dsn=SENTRY_DSN_BED,
    integrations=[DjangoIntegration(), sentry_logging],
    release=SENTRY_RELEASE,
    environment=SENTRY_ENVIRONMENT,
)

# CSP is not currently configured for madewithwagtail, so this is
# a no-op, but might as well leave it in case they do
CSP_REPORT_URI = [
    "{base_url}&sentry_release={release}&sentry_environment={environment}".format(
        base_url=SENTRY_CSP_URL, release=SENTRY_RELEASE, environment=SENTRY_ENVIRONMENT
    )
]

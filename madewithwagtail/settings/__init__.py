from typed_environment_configuration import *

_ENVVARS = [
    StringVariable("PROJECT"),  # Project namespace
    StringVariable(
        "ENVIRONMENT"
    ),  # Application environment i.e. development, production, etc.
    StringVariable(
        "APPLICATION_VERSION"
    ),  # The Application version used across project
    StringListVariable("ADDRESSES", default=""),
    StringVariable("AWS_STORAGE_BUCKET_NAME", default=""),  # S3 Bucket Name
    StringVariable("AWS_S3_CUSTOM_DOMAIN", default=""),  # S3 Domain
    StringVariable("DATABASE_URL"),  # e.g. postgres URL
    StringVariable("WAGTAILCMS_TWIW_SLACK_HOOK", default=""),
    StringVariable("RECAPTCHA_PUBLIC_KEY", default=""),
    StringVariable("RECAPTCHA_PRIVATE_KEY", default=""),
    StringVariable("GOOGLE_MAPS_API_KEY", default=""),
    StringVariable("GOOGLE_ANALYTICS_KEY", default=""),
]

_APP_ENVVARS = [StringVariable("APP_SECRET_KEY")]


_DJANGO_ENVVARS = [
    BoolVariable("DJANGO_DEBUG", default=False),
    StringVariable("DJANGO_SERVER_ENV", default="Nonprod"),
]


def fill(variables, v, prefix=""):
    for var in variables:
        v[var.name] = var.getenv(prefix=prefix)


fill(_ENVVARS, vars())
fill(_APP_ENVVARS, vars(), "APP_")
fill(_DJANGO_ENVVARS, vars(), "DJANGO_")

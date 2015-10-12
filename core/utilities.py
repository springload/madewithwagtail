from django.conf import settings
from django.core.exceptions import ValidationError
#  A place to define methods used in different parts of the app


def validate_only_one_instance(obj):
    """
    Allow only one instance
    """
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("We're sorry but a %s already exists, only one is allowed." % model.__name__)


def replace_tags(string=None, tags=dict()):
    """
    Replace tags from a given string
    """
    if string is None:
        raise TypeError("string type needed")
    else:
        for key, value in tags.items():
            string = string.replace(key, value)
    return string


def has_recaptcha():
    """
    Check if the WagtailCaptcha settings are properly set
    """
    wagtailcaptcha_public_key = getattr(settings, 'RECAPTCHA_PUBLIC_KEY', None)
    wagtailcaptcha_private_key = getattr(settings, 'RECAPTCHA_PRIVATE_KEY', None)

    return wagtailcaptcha_public_key and wagtailcaptcha_private_key

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from wagtail.wagtailcore.models import Page


def custom_user_can_edit_content_type(user, content_type):
    """
    Returns boolean value indicating if the given user has any permission related to the given
    content type
    """
    # True if user is superadmin
    if user.is_active and user.is_superuser:
        return True

    # Check if content_type is Page or inherits Page
    if (issubclass(content_type, Page)):
        content_type_instances = content_type.objects.all()
        if len(content_type_instances) > 0:
            content_type_instance = content_type_instances[0]
            permission_checker = content_type_instance.permissions_for_user(user)
            return permission_checker.can_edit()
        else:
            return False

    # If it gets to this point it's probably a Snippet model, check if edit/add/delete (exclusive)
    ct = ContentType.objects.get_for_model(content_type)
    permissions = Permission.objects.filter(content_type=ct).select_related('content_type')

    if len(permissions) > 0:
        # At least has one permission, either add/change/delete we return True with the first we find,
        # without caring which one it is
        for perm in permissions:
            permission_name = "%s.%s" % (perm.content_type.app_label, perm.codename)
            if user.has_perm(permission_name):
                return True
    # If we got here nothing else to do but deny permission
    return False

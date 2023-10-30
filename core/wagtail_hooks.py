from django.conf import settings
from django.utils.html import format_html_join

from wagtail import hooks


@hooks.register("insert_editor_css")
def editor_css():
    """
    Add extra CSS files to the admin
    """
    css_files = [
        "wagtailadmin/css/admin.css",
    ]

    css_includes = format_html_join(
        "\n",
        '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files),
    )

    return css_includes

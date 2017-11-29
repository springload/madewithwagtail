from django.conf import settings
from django.utils.html import format_html_join
from wagtail.wagtailadmin.rich_text import HalloPlugin
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, check_url


@hooks.register('insert_editor_css')
def editor_css():
    """
    Add extra CSS files to the admin
    """
    css_files = [
        'wagtailadmin/css/admin.css',
    ]

    css_includes = format_html_join(
        '\n', '<link rel="stylesheet" href="{0}{1}">', ((settings.STATIC_URL, filename) for filename in css_files))

    return css_includes


@hooks.register('register_rich_text_features')
def register_cleanhtml_feature(features):
    features.register_editor_plugin(
        'hallo', 'cleanhtml',
        HalloPlugin(
            name='hallocleanhtml',
            js=[
                'wagtailadmin/js/vendor/jquery.htmlClean.min.js',
                'wagtailadmin/js/vendor/rangy-selectionsaverestore.js',
            ],
            options={
                'format': False,
                'allowedTags': [
                    'p', 'em', 'strong', 'div', 'ol', 'ul', 'li', 'a', 'figure', 'blockquote', 'cite', 'img'],
                'allowedAttributes': ['style'],
            }
        )
    )


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    """
    Whitelist custom elements to the hallo.js editor
    """
    return {
        'a': attribute_rule({'href': check_url, 'class': True}),
    }

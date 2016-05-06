from django.utils.html import format_html_join
from django.conf import settings

from wagtail.wagtailcore.whitelist import attribute_rule
from wagtail.wagtailcore.whitelist import check_url
from wagtail.wagtailcore.whitelist import allow_without_attributes
from wagtail.wagtailcore import hooks


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


@hooks.register('insert_editor_js')
def editor_js():
    """
    Add extra JS files to the admin
    """
    js_files = [
        'wagtailadmin/js/vendor/jquery.htmlClean.min.js',
        'wagtailadmin/js/vendor/rangy-selectionsaverestore.js',
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}{1}"></script>', ((settings.STATIC_URL, filename) for filename in js_files))

    return js_includes + """<script type="text/javascript">
        registerHalloPlugin('hallocleanhtml', {
            format: false,
            allowedTags: ['h2', 'h3', 'h4', 'h5', 'p', 'em', 'strong', 'br', 'div', 'ol', 'ul', \
              'li', 'a', 'figure', 'embed', 'blockquote', 'cite', 'img'],
            allowedAttributes: ['style']
        });
        </script>"""


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    """
    Whitelist custom elements to the hallo.js editor
    """
    return {
        'a': attribute_rule({'href': check_url, 'class': True}),
    }

from django.utils.html import format_html
from wagtail.wagtailadmin.menu import MenuItem
from core.permissions import custom_user_can_edit_content_type


class FontAwesomeMenuItem(MenuItem):
    def __init__(self, content_type, label, url, name=None, classnames='', attrs=None, order=1000):
        self.content_type = content_type
        return super(FontAwesomeMenuItem, self).__init__(label, url, name, classnames, attrs, order)

    """
    Class for icons using the FontAwesome external lib http://fortawesome.github.io/Font-Awesome/
    """
    def render_html(self, request):
        return format_html(
            """<li class="menu-{0}"><a href="{1}" {3}><i class="{2}"></i>{4}</a></li>""",
            self.name, self.url, self.classnames, self.attr_string, self.label)

    def is_shown(self, request):
        return custom_user_can_edit_content_type(request.user, self.content_type)

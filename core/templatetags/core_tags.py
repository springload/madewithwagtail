from django import template
from django.core.exceptions import ObjectDoesNotExist

from core.models import NavigationMenu, Page
import urllib

register = template.Library()


@register.inclusion_tag('core/includes/menu.html', takes_context=True)
def menu(context, name=None, current_page=None):
    """
    Retrieves the MenuElement(s) under the NavigationMenu with given menu_name
    """
    if name is None or current_page is None:
        return None
    try:
        menu_items = NavigationMenu.objects.get(menu_name=name).items

        if current_page:
            for item in menu_items:
                if item.link_page and item.link_page.id == current_page.id:
                    item.is_active = True
    except ObjectDoesNotExist:
        return None

    return {
        'links': menu_items,
        'request': context['request'],
    }


@register.inclusion_tag('core/includes/footer_menu.html', takes_context=True)
def footer_menu(context, name=None, current_page=None):
    """
    Retrieves the MenuElement(s) under the NavigationMenu with given menu_name
    """
    if name is None or current_page is None:
        return None
    try:
        menu_items = NavigationMenu.objects.get(menu_name=name).items

    except ObjectDoesNotExist:
        return None

    return {
        'links': menu_items,
        'request': context['request'],
    }


@register.filter
def content_type(model):
    """
    Return the model name/"content type" as a string e.g BlogPage, NewsListingPage.
    Can be used with "slugify" to create CSS-friendly classnames
    Usage: {{ self|content_type|slugify }}
    """
    return model.__class__.__name__


class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


@register.tag(name='set')
def set_var(parser, token):
    """
    {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])


@register.inclusion_tag('core/includes/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(
            self, inclusive=True).filter(depth__gt=2)
    return {
        'ancestors': ancestors,
        'request': context['request'],
    }


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def subtract(value, arg):
    return value - arg


@register.simple_tag
def build_qsa(page_number, tag, query_string):
    qsa = {}
    if page_number:
        qsa['page'] = page_number
    if tag:
        qsa['tag'] = tag
    if query_string:
        qsa['q'] = query_string
    return "?" + urllib.urlencode(qsa)

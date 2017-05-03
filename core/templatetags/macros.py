from django import template, VERSION
from django.template.loader import get_template


if VERSION[:3] >= (1, 8, 0):
    from django.template.base import FilterExpression
else:
    from django.template import FilterExpression

register = template.Library()


def _setup_macros_dict(parser):
    """
    Metadata of each macro are stored in a new attribute
    of 'parser' class. That way we can access it later
    in the template when processing 'usemacro' tags.
    """
    try:
        # Only try to access it to eventually trigger an exception
        parser._macros
    except AttributeError:
        parser._macros = {}


class DefineMacroNode(template.Node):
    def __init__(self, name, nodelist, args):

        self.name = name
        self.nodelist = nodelist
        self.args = []
        self.kwargs = {}
        for a in args:
            if "=" not in a:
                self.args.append(a)
            else:
                name, value = a.split("=")
                self.kwargs[name] = value

    def render(self, context):
        # empty string - {% macro %} tag does no output
        return ''


@register.tag(name="macro")
def do_macro(parser, token):
    try:
        args = token.split_contents()
        tag_name, macro_name, args = args[0], args[1], args[2:]
    except IndexError:
        m = ("'%s' tag requires at least one argument (macro name)"
            % token.contents.split()[0])
        raise template.TemplateSyntaxError(m)
    # TODO: could do some validations here,
    # for now, "blow your head clean off"
    nodelist = parser.parse(('endmacro', ))
    parser.delete_first_token()
    _setup_macros_dict(parser)
    parser._macros[macro_name] = DefineMacroNode(macro_name, nodelist, args)
    return parser._macros[macro_name]


class LoadMacrosNode(template.Node):
    def render(self, context):
        # empty string - {% loadmacros %} tag does no output
        return ''


@register.tag(name="loadmacros")
def do_loadmacros(parser, token):
    # In Django 1.7 get_template() returned a django.template.Template.
    # In Django 1.8 it returns a django.template.backends.django.Template.
    try:
        tag_name, filename = token.split_contents()
    except IndexError:
        m = ("'%s' tag requires at least one argument (macro name)" % token.contents.split()[0])
        raise template.TemplateSyntaxError(m)
    if filename[0] in ('"', "'") and filename[-1] == filename[0]:
        filename = filename[1:-1]
    t = get_template(filename)
    nodelist = t.template.nodelist
    macros = nodelist.get_nodes_by_type(DefineMacroNode)
    _setup_macros_dict(parser)
    for macro in macros:
        parser._macros[macro.name] = macro
    return LoadMacrosNode()


class UseMacroNode(template.Node):

    def __init__(self, macro, fe_args, fe_kwargs, context_only):
        self.macro = macro
        self.fe_args = fe_args
        self.fe_kwargs = fe_kwargs
        self.context_only = context_only

    def render(self, context):

        for i, arg in enumerate(self.macro.args):
            try:
                fe = self.fe_args[i]
                context[arg] = fe.resolve(context)
            except IndexError:
                context[arg] = ""

        for name, default in self.macro.kwargs.items():
            if name in self.fe_kwargs:
                context[name] = self.fe_kwargs[name].resolve(context)
            else:
                context[name] = FilterExpression(default,
                                                 self.macro.parser
                                                 ).resolve(context)

        # Place output into context variable
        context[self.macro.name] = self.macro.nodelist.render(context)
        return '' if self.context_only else context[self.macro.name]


def parse_usemacro(parser, token):
    try:
        args = token.split_contents()
        macro_name, values = args[1], args[2:]
    except IndexError:
        m = ("'%s' tag requires at least one argument (macro name)"
             % token.contents.split()[0])
        raise template.TemplateSyntaxError(m)

    try:
        macro = parser._macros[macro_name]
    except (AttributeError, KeyError):
        m = "Macro '%s' is not defined" % macro_name
        raise template.TemplateSyntaxError(m)

    fe_kwargs = {}
    fe_args = []

    for val in values:
        if "=" in val:
            # kwarg
            name, value = val.split("=")
            fe_kwargs[name] = FilterExpression(value, parser)
        else:  # arg
            # no validation, go for it ...
            fe_args.append(FilterExpression(val, parser))

    macro.name = macro_name
    macro.parser = parser
    return macro, fe_args, fe_kwargs


@register.tag(name="usemacro")
def do_usemacro(parser, token):
    return UseMacroNode(*parse_usemacro(parser, token), context_only=False)


@register.tag(name="setmacro")
def do_setmacro(parser, token):
    return UseMacroNode(*parse_usemacro(parser, token), context_only=True)

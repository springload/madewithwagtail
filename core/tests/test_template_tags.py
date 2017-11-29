from bs4 import BeautifulSoup
from django.template import Context, Template

from core.models import HomePage
from core.tests.utils import WagtailTest


class TemplateTagsTestCase(WagtailTest):

    def setUp(self):
        super(TemplateTagsTestCase, self).setUp()
        self.home_page = HomePage.objects.all()[0]

    def test_set_var(self):
        """
        Test set_var(parser, token) tag
        {% set <var_name>  = <var_value> %}

        """
        # We just assign a simple string to a ver and check it gets printed nicely
        rendered = Template("{% load core_tags %}{% set x = 'The hammer of Zeus' %}{{ x }}").render(Context({}))
        self.assertEqual(rendered, "The hammer of Zeus")

    def test_footer_menu(self):
        """
        Test footer_menu(context) tag
        {% footer_menu %}

        """
        response = self.client.get(self.home_page.url)

        # Render and check footer has 2 items
        template_str = "{% load core_tags %}{% footer_menu name='Footer' current_page=self.home_page %}"
        rendered = Template(template_str).render(Context({"request": response.request}))
        soup = BeautifulSoup(rendered, 'html5lib')

        self.assertEqual(
            len(soup.findAll("a")),
            4  # Number of links in the footer, should be 4 but fixtures are bit outdated
        )

    def test_main_menu(self):
        """
        Test main_menu(context) tag
        {% main_menu %}

        """
        response = self.client.get(self.home_page.url)

        # Render and check footer has 2 items
        template_str = "{% load core_tags %}{% menu name='Main' current_page=self.home_page %}"
        rendered = Template(template_str).render(Context({"request": response.request}))

        soup = BeautifulSoup(rendered, 'html5lib')

        self.assertEqual(
            len(soup.findAll("a")),
            5  # Number of links in the main nav
        )

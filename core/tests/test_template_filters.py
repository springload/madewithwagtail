from django.template import Context, Template

from core.tests.utils import *
from core.models import *


class TemplateFiltersTestCase(WagtailTest):

    def setUp(self):
        super(TemplateFiltersTestCase, self).setUp()

    def test_content_type(self):
        """
        Test content_type filter
        {{ page|content_type }}

        """
        self.homepage = HomePage.objects.all()[0]
        rendered = Template("{% load core_tags %}{{ homepage|content_type }}") \
            .render(Context({"homepage": self.homepage}))

        self.assertEqual('HomePage', rendered)

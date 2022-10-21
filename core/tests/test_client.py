from taggit.models import Tag

from core.models import HomePage, WagtailSitePage
from core.tests.utils import WagtailTest


class ClientTestCase(WagtailTest):
    def setUp(self):
        super(ClientTestCase, self).setUp()

    def testHomePage(self):
        home_page = HomePage.objects.all()[0]
        response = self.client.get(home_page.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, home_page.template)
        # Check it comes with the appropiate number of pages
        pages = WagtailSitePage.objects.live().descendant_of(home_page)
        self.assertEqual(response.context["pages"].paginator.count, pages.count())
        self.assertContains(
            response,
            "one-half--medium one-third--large",
            count=response.context["pages"].paginator.count,
        )
        # Check the first page is featured
        self.assertEqual(response.context["pages"][0].is_featured, True)
        # Check the tags are printed
        tags = Tag.objects.all().filter(
            core_pagetag_items__isnull=False,
            core_pagetag_items__content_object__live=True,
        )

        self.assertContains(response, "btn -tag", count=tags.count())

# from wagtail.tests.utils import WagtailPageTests
# from wagtail.tests.utils.form_data import nested_form_data, streamfield, rich_text
# from core.models import *
#
# class HomePageTests(WagtailPageTests):
#     def test_can_create_a_page(self):
#         root_page = HomePage.objects.get(pk=2)
#         self.assertCanCreate(root_page, HomePage, nested_form_data({
#             'title': 'Made with wagtail home',
#             'body': rich_text('<p>Potato is my favourite vegetable</p>')
#         }))
#

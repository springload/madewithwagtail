import core.tests.utils as test_utils
from core import models


class WagtailCompanyPageTestCase(test_utils.WagtailTest):

    def test_twitter_handler(self):
        twitter_user = 'springloadnz'
        twitter_url = 'https://twitter.com/{}'.format(twitter_user)
        twitter_handle = '@{}'.format(twitter_user)

        page = models.WagtailCompanyPage(title='Springload', twitter_url=twitter_url)

        self.assertEqual(page.twitter_handler, twitter_handle)

    def test_twitter_handler_with_trailing_slash(self):
        twitter_user = 'springloadnz'
        twitter_url = 'https://twitter.com/{}/'.format(twitter_user)
        twitter_handle = '@{}'.format(twitter_user)

        page = models.WagtailCompanyPage(title='Springload', twitter_url=twitter_url)

        self.assertEqual(page.twitter_handler, twitter_handle)

    def test_twitter_handler_with_no_url(self):
        page = models.WagtailCompanyPage(title='Springload')

        self.assertIsNone(page.twitter_handler)

    def test_github_user(self):
        github_user = 'springload'
        github_url = 'https://github.com/{}'.format(github_user)

        page = models.WagtailCompanyPage(title='Springload', github_url=github_url)

        self.assertEqual(page.github_user, github_user)

    def test_github_user_with_trailing_slash(self):
        github_user = 'springload'
        github_url = 'https://github.com/{}/'.format(github_user)

        page = models.WagtailCompanyPage(title='Springload', github_url=github_url)

        self.assertEqual(page.github_user, github_user)

    def test_github_user_with_no_url(self):
        page = models.WagtailCompanyPage(title='Springload')

        self.assertIsNone(page.github_user)

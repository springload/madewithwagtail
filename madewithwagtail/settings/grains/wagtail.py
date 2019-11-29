from madewithwagtail.settings.grains.django import ALLOWED_HOSTS

WAGTAIL_SITE_NAME = "Made with Wagtail"

# Search results template
WAGTAILSEARCH_RESULTS_TEMPLATE = 'core/search_results.html'

# Limit image upload size due to RAM constraints on containers
WAGTAILIMAGES_MAX_IMAGE_PIXELS = 30 * 1000 ** 2  # 30MP size limit

# BASE_URL is only used in emails from the wagtailadmin that
# are sent in a non-request-context, fixes moderation emails
# according to https://github.com/wagtail/wagtail/issues/826
if ALLOWED_HOSTS and ALLOWED_HOSTS[0] != "*":
    BASE_URL = "https://" + ALLOWED_HOSTS[0]

LOGIN_URL = 'wagtailadmin_login'
LOGIN_REDIRECT_URL = 'wagtailadmin_home'

# Wagtailgmaps settings
WAGTAIL_ADDRESS_MAP_CENTER = 'Wellington, New Zealand'
WAGTAIL_ADDRESS_MAP_ZOOM = 8
WAGTAIL_ADDRESS_MAP_KEY = GOOGLE_MAPS_API_KEY

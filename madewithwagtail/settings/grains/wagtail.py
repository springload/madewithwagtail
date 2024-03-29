from typed_environment_configuration import *

from madewithwagtail.settings import *
from madewithwagtail.settings.grains.django import ALLOWED_HOSTS

GOOGLE_MAPS_API_KEY = StringVariable("GOOGLE_MAPS_API_KEY", default="").getenv()

WAGTAIL_SITE_NAME = "Made with Wagtail"

# Search results template
WAGTAILSEARCH_RESULTS_TEMPLATE = "core/search_results.html"

# Limit image upload size due to RAM constraints on containers
WAGTAILIMAGES_MAX_IMAGE_PIXELS = 30 * 1000**2  # 30MP size limit

# BASE_URL is only used in emails from the wagtailadmin that
# are sent in a non-request-context, fixes moderation emails
# according to https://github.com/wagtail/wagtail/issues/826
if ALLOWED_HOSTS and ALLOWED_HOSTS[0] != "*":
    BASE_URL = "https://" + ALLOWED_HOSTS[0]

LOGIN_URL = "wagtailadmin_login"
LOGIN_REDIRECT_URL = "wagtailadmin_home"

# Wagtailgmaps settings
WAGTAIL_ADDRESS_MAP_CENTER = "Wellington, New Zealand"
WAGTAIL_ADDRESS_MAP_ZOOM = 8
WAGTAIL_ADDRESS_MAP_KEY = GOOGLE_MAPS_API_KEY

# Responsive HTML for embeds
# according to https://docs.wagtail.org/en/v2.16.1/releases/2.8.html#responsive-html-for-embeds-no-longer-added-by-default
WAGTAILEMBEDS_RESPONSIVE_HTML = True

WAGTAILADMIN_STATIC_FILE_VERSION_STRINGS = True

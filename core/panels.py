from wagtailgmaps.edit_handlers import MapFieldPanel

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Page

HOME_PAGE_CONTENT_PANELS = [
    FieldPanel("title", classname="full title"),
    FieldPanel("body", classname="full"),
]

WAGTAIL_PAGE_CONTENT_PANELS = HOME_PAGE_CONTENT_PANELS + [
    FieldPanel("tags"),
]

WAGTAIL_PAGE_PROMOTE_PANELS = [
    MultiFieldPanel(Page.promote_panels, "SEO and metadata fields"),
    FieldPanel("feed_image"),
]

WAGTAIL_SITE_PAGE_PROMOTE_PANELS = [
    FieldPanel("is_featured"),
] + WAGTAIL_PAGE_PROMOTE_PANELS


WAGTAIL_SITE_PAGE_CONTENT_PANELS = [
    FieldPanel("title", classname="full title"),
    FieldPanel("site_url"),
    FieldPanel("site_screenshot"),
    FieldPanel("body", classname="full"),
    FieldPanel("tags"),
    FieldPanel("in_cooperation_with"),
]

WAGTAIL_COMPANY_PAGE_CONTENT_PANELS = HOME_PAGE_CONTENT_PANELS + [
    FieldPanel("location"),
    FieldPanel("company_url"),
    FieldPanel("github_url"),
    FieldPanel("twitter_url"),
    FieldPanel("logo"),
    FieldPanel("tags"),
    MultiFieldPanel(
        [
            FieldPanel("show_map"),
            MapFieldPanel("coords", latlng=True),
        ],
        heading="Coordinates",
    ),
]

WAGTAIL_COMPANY_PAGE_SETTINGS_PANELS = Page.settings_panels + [
    FieldPanel("sites_ordering"),
]

WAGTAIL_COMPANY_INDEX_PAGE_CONTENT_PANELS = Page.content_panels + [
    FieldPanel("show_map"),
    FieldPanel("body", classname="full"),
]

SUBMIT_FORM_PAGE_CONTENT_PANELS = [
    FieldPanel("title", classname="full title"),
    FieldPanel("body", classname="full"),
    FieldPanel("thank_you_text", classname="full"),
    InlinePanel("form_fields", label="Form fields"),
    MultiFieldPanel(
        [
            FieldPanel("to_address"),
            FieldPanel("from_address"),
            FieldPanel("subject"),
        ],
        "Email notification",
    ),
]

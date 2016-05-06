from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.models import Page


HOME_PAGE_CONTENT_PANELS = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full")
]

WAGTAIL_PAGE_CONTENT_PANELS = HOME_PAGE_CONTENT_PANELS + [
    FieldPanel('tags'),
]

WAGTAIL_PAGE_PROMOTE_PANELS = [
    MultiFieldPanel(Page.promote_panels, "SEO and metadata fields"),
    ImageChooserPanel('feed_image'),
]

WAGTAIL_SITE_PAGE_PROMOTE_PANELS = [
    FieldPanel('is_featured'),
] + WAGTAIL_PAGE_PROMOTE_PANELS


WAGTAIL_SITE_PAGE_CONTENT_PANELS = [
    FieldPanel('title', classname="full title"),
    FieldPanel('site_url'),
    ImageChooserPanel('image_desktop'),
    ImageChooserPanel('image_tablet'),
    ImageChooserPanel('image_phone'),
    FieldPanel('body', classname="full"),
    FieldPanel('tags'),
]

WAGTAIL_COMPANY_PAGE_CONTENT_PANELS = HOME_PAGE_CONTENT_PANELS + [
    FieldPanel('location'),
    FieldPanel('company_url'),
    FieldPanel('github_url'),
    FieldPanel('twitter_url'),
    ImageChooserPanel('logo'),
    FieldPanel('tags'),
]

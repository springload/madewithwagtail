import re

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings

from slackweb import Slack

from wagtail.wagtailcore.models import PageRevision
from wagtail.wagtailcore.signals import page_published

from core.models import WagtailPage, WagtailSitePage
from core.utilities import replace_tags

# Signals for Models. Some for performing specific class tasks, some just for clearing the cache.

# Set your own classes
PAGE_CLASSES = [WagtailPage]


@receiver(pre_save)
def pre_page_save(sender, instance, **kwargs):
    """
    Strip empty <p> elements from any RichTextField and other stuff when saved instance is one of the following
    classes: defined in PAGE_CLASSES
    """
    if (kwargs.get('created', True) and not kwargs.get('raw', False)):
        if (sender in PAGE_CLASSES):
            for field in instance._meta.fields:
                if sender._meta.get_field(field.name).__class__.__name__ == "RichTextField":
                    field_to_string = getattr(instance, field.name)
                    field_to_string = re.sub(r"\n", "", field_to_string)
                    # Clean empty paragraphs
                    field_to_string = re.sub(r"<p>(<br/>|<br>)*</p>", "", field_to_string)
                    # Wrap images and embeds into figures instead of paragraphs
                    field_to_string = re.sub(
                        r"<p>((<img.+/.[^>]+>)|(<embed.[^>]+embedtype=\"image\".[^>]+/>))+:?(<br>|<br/>)*</p>",
                        r"<figure>\1</figure>",
                        field_to_string
                    )
                    clean_field = replace_tags(
                        field_to_string, {"<b>": "<strong>", "<i>": "<em>", "</b>": "</strong>", "</i>": "</em>"}
                    )
                    #  Replace content field
                    setattr(instance, field.name, clean_field)


@receiver(pre_save, sender=PageRevision)
def pre_page_revision_save(sender, instance, **kwargs):
    """
    Strip empty <p> elements from any RichTextField only when related page is a WagtailPage
    """
    if (kwargs.get('created', True) and not kwargs.get('raw', False)):
        if isinstance(instance.page, WagtailPage):
            mirror_page = instance.as_page_object()
            for field in mirror_page._meta.fields:
                if instance.page._meta.get_field(field.name).__class__.__name__ == "RichTextField":
                    field_to_string = getattr(mirror_page, field.name)
                    field_to_string = re.sub(r"\n", "", field_to_string)
                    # Clean empty paragraphs
                    field_to_string = re.sub(r"<p>(<br/>|<br>)*</p>", "", field_to_string)
                    # Wrap images and embeds into figures instead of paragraphs
                    field_to_string = re.sub(
                        r"<p>((<img.+/.[^>]+>)|(<embed.[^>]+embedtype=\"image\".[^>]+/>))+:?(<br>|<br/>)*</p>",
                        r"<figure>\1</figure>",
                        field_to_string
                    )
                    clean_field = replace_tags(
                        field_to_string, {"<b>": "<strong>", "<i>": "<em>", "</b>": "</strong>", "</i>": "</em>"}
                    )
                    #  Replace content field
                    setattr(mirror_page, field.name, clean_field)
                    #  To json again
                    instance.content_json = mirror_page.to_json()


@receiver(post_save)
def post_model_save(sender, instance, **kwargs):
    """
    Clear cache when any kind of Model is saved
    """
    cache.clear()


@receiver(page_published, sender=WagtailSitePage)
def send_to_slack(sender, **kwargs):
    url = getattr(settings, 'PUBLISH_SLACK_HOOK', None)
    if not url:
        return

    page = kwargs['instance']
    Slack(url).send({
        'text': 'New site published! Check out *%s* :rocket:' % page.title,
        'username': 'Made with Wagtail',
        'icon_emoji': ':bird:',
        'attachments': [
            {
                'fallback': '%s - %s' % (page.title, page.site_url),
                'title': page.title,
                'text': page.full_url,
                'color': '#43b1b0',
            }
        ]
    })

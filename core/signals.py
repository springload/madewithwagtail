from datetime import timedelta
import re

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings
from django.utils.encoding import force_text

from slackweb import Slack

import tweepy
import os

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

# this sends an update to the slack channel @madewithwagtail
@receiver(page_published, sender=WagtailSitePage)
def send_to_slack(sender, **kwargs):
    hooks = getattr(settings, 'PUBLISH_SLACK_HOOKS', [])
    if not hooks:
        return

    page = kwargs['instance']
    # It is the first publish if there is no time between first publish and latest revision.
    published_since = page.latest_revision_created_at - page.first_published_at
    # Add a 5 sec delta to account for slowness of the server.
    is_first_publish = published_since <= timedelta(seconds=5)

    if is_first_publish:
        for hook in hooks:
            Slack(hook).send({
                'text': 'New site published! :rocket:',
                'username': 'Made with Wagtail',
                'icon_emoji': ':bird:',
                'attachments': [
                    {
                        'fallback': force_text(page),
                        'title': page.title,
                        'text': page.full_url,
                        'color': '#43b1b0',
                    }
                ]
            })

# this makes a tweet on twitter profile @MadeWithWagtail
@receiver(page_published, sender=WagtailSitePage)
def send_to_twitter(sender, **kwargs):

    page = kwargs['instance']
    # It is the first publish if there is no time between first publish and latest revision.
    published_since = page.latest_revision_created_at - page.first_published_at
    # Add a 5 sec delta to account for slowness of the server.
    is_first_publish = published_since <= timedelta(seconds=5)

    if is_first_publish:

        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)

        maxTweetLength = 140
        prefix = "New site on MWW! Welcome '"
        url = page.url
        titleSuffix = "' "
        ellipsis = '\u2026'
        handle = ""

        # if the submission contains a twitter handle, add this to the end of the tweet
        parent_page = page.get_parent().specific
        if parent_page.twitter_handler:
            handle = " by " + parent_page.twitter_handler

        urlMaxSize = 23
        remainingTweetLength = maxTweetLength - len(prefix) - len(handle) - min([len(url), urlMaxSize]) - len(titleSuffix)

        if len(page.title) > remainingTweetLength:
            remainingTweetLength -= len(ellipsis)
            truncatedTitle = page.title[0:remainingTweetLength]
            endOfWordIndex = max([truncatedTitle.rfind(' '), truncatedTitle.rfind('.')])
            truncatedTitle = truncatedTitle[0:endOfWordIndex]
            title = truncatedTitle + ellipsis
        else:
            title = page.title

        tweet = prefix + title + titleSuffix + url + handle

        # full tweet format that includes the status and image
        api.update_with_media(page.image_desktop.file.name, tweet, file=page.image_desktop.file);





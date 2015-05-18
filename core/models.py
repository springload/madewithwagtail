import os
import re

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import django.db.models.options as options
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

from taggit.models import TaggedItemBase, Tag

from bs4 import BeautifulSoup

from core.utilities import *
from core.snippets import *
from core.forms import *

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)


class IndexPage(models.Model):

    """
    Abstract Index Page class. Declare a couple of abstract methods that should be implemented by
    any class implementing this interface.
    """
    # Just one instance allowed

    def clean(self):
        validate_only_one_instance(self)

    def children(self):
        raise NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))

    def get_context(self, request):
        raise NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))

    class Meta:
        abstract = True


class HomePage(Page, IndexPage):

    """
    HomePage class, inheriting from wagtailcore.Page straight away
    """
    subpage_types = [
        'core.WagtailPage',
        'core.CompanyIndex',
        'core.WagtailCompanyPage',
        'core.WagtailSitePage',
        'core.SubmitFormPage'
    ]
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    search_fields = ()

    body = RichTextField(blank=True)

    @property
    def og_image(self):
        # Returns image and image type of feed_image, if exists
        image = {'image': None, 'type': None}
        if self.feed_image:
            image['image'] = self.feed_image
        name, extension = os.path.splitext(image['image'].file.url)
        image['type'] = extension[1:]
        return image

    def children(self):
        return self.get_children().live()

    def get_context(self, request):
        # Get pages
        pages = WagtailSitePage.objects.live().descendant_of(self).order_by('-is_featured', '-latest_revision_created_at')

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            pages = pages.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(pages, 12)  # Show 12 pages per page
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        # Update template context
        context = super(HomePage, self).get_context(request)
        context['pages'] = pages
        # Only tags used by live pages
        context['tags'] = Tag.objects.filter(
            core_pagetag_items__isnull=False,
            core_pagetag_items__content_object__live=True
        ).distinct().order_by('name')

        return context

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Home page"
        description = "Where the good stuff happens!"


HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full")
]

HomePage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "SEO and metadata fields"),
    ImageChooserPanel('feed_image'),
]


class CompanyIndex(Page, IndexPage):

    """
    HomePage class, inheriting from wagtailcore.Page straight away
    """
    subpage_types = ['core.WagtailCompanyPage']
    search_fields = ()
    body = RichTextField(null=True, blank=True)

    def children(self):
        return self.get_children().live()

    def get_context(self, request):
        # Get pages
        pages = WagtailCompanyPage.objects.live().descendant_of(self).distinct().order_by('-numchild', '-latest_revision_created_at')

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            pages = pages.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(pages, 12)  # Show 12 pages per page
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        # Update template context
        context = super(CompanyIndex, self).get_context(request)
        context['pages'] = pages
        return context

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Company Pages"
        description = "Companies index"

CompanyIndex.content_panels = Page.content_panels + [FieldPanel('body', classname="full")]


class PageTag(TaggedItemBase):
    content_object = ParentalKey('core.WagtailPage', related_name='tagged_items')


# Main core Page model. All main content pages inherit from this class.
class WagtailPage(Page):

    """
    Our main custom Page class. All content pages should inherit from this one.
    """
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=PageTag, blank=True)
    search_fields = ()

    @property
    def parent(self):
        try:
            return self.get_ancestors().reverse()[0]
        except ObjectDoesNotExist:
            return None
        except IndexError:
            return None

    @property
    def child(self):
        for related_object in self._meta.get_all_related_objects():
            if not issubclass(related_object.model, self.__class__):
                continue
            try:
                return getattr(self, related_object.get_accessor_name())
            except ObjectDoesNotExist:
                pass

    @property
    def body_text(self):
        return BeautifulSoup(self.body).get_text()

    @property
    def body_excerpt(self):
        """
        Return body text replacing end of lines (. ? ! chars) with a blank space
        """
        return re.sub(r'([\.?!])([a-zA-Z])', r'\1 \2', self.body_text)

    @property
    def og_image(self):
        # Returns image and image type of feed_image or image as fallback, if exists
        image = {'image': None, 'type': None}
        if self.feed_image:
            image['image'] = self.feed_image
        name, extension = os.path.splitext(image['image'].file.url)
        image['type'] = extension[1:]
        return image

WagtailPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
    FieldPanel('tags'),
]

WagtailPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "SEO and metadata fields"),
    ImageChooserPanel('feed_image'),
]


class WagtailCompanyPage(WagtailPage):
    """
    Company page listing abunch of site pages
    """
    parent_types = ['core.HomePage']
    subpage_types = ['core.WagtailSitePage']

    company_url = models.URLField(
        blank=True,
        null=True,
        help_text='Paste the URL of your site, something like "http://www.springload.co.nz"',
    )
    github_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=128, blank=True, null=True)

    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (  # Inherit search_fields from Page
        index.SearchField('company_url', boost=1),
        index.SearchField('body_text', boost=1)
    )

    @property
    def twitter_handler(self):
        if self.twitter_url:
            return "@%s" % self.twitter_url.split("/")[-1]
        else:
            return None

    @property
    def github_user(self):
        if self.github_url:
            return self.github_url.split("/")[-1]
        else:
            return None

    @property
    def og_image(self):
        # Returns image and image type of logo or feed_image as fallback, if exists
        image = {'image': None, 'type': None}
        if self.logo:
            image['image'] = self.logo
        elif self.feed_image:
            image['image'] = self.feed_image
        name, extension = os.path.splitext(image['image'].file.url)
        image['type'] = extension[1:]
        return image

    def children(self):
        return WagtailSitePage.objects.live().descendant_of(self)

    def get_context(self, request):
        # Get pages
        pages = self.children()
        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(pages, 12)  # Show 12 pages per page
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        # Update template context
        context = super(WagtailCompanyPage, self).get_context(request)
        context['pages'] = pages
        return context

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Company page"
        description = "Page for companies developing Wagtail"

WagtailCompanyPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
    FieldPanel('location'),
    FieldPanel('company_url'),
    FieldPanel('github_url'),
    FieldPanel('twitter_url'),
    ImageChooserPanel('logo'),
    FieldPanel('tags'),
]


class WagtailSitePage(WagtailPage):
    """
    Site page
    """
    parent_types = ['core.WagtailCompanyPage', 'core.HomePage']
    subpage_types = []
    is_featured = models.BooleanField(
        "Featured",
        default=False,
        blank=False,
        help_text='''If enabled, this site will appear on top of the sites list of the homepage.'''
    )
    image_desktop = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image_tablet = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image_phone = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    site_url = models.URLField(
        blank=False,
        null=True,
        help_text='Paste the URL of your site, something like "http://www.springload.co.nz"',
    )

    search_fields = Page.search_fields + (  # Inherit search_fields from Page
        index.SearchField('site_url'),
        index.SearchField('body_text')
    )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Site page"
        description = "Page to show case an existing site based on Wagtail"

WagtailSitePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('site_url'),
    ImageChooserPanel('image_desktop'),
    ImageChooserPanel('image_tablet'),
    ImageChooserPanel('image_phone'),
    FieldPanel('body', classname="full"),
    FieldPanel('tags'),
]

WagtailSitePage.promote_panels = [FieldPanel('is_featured'), ] + WagtailPage.promote_panels

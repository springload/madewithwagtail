import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images import urls as wagtailimages_urls
from wagtail.search.signal_handlers import (
    register_signal_handlers as wagtailsearch_register_signal_handlers,
)

from api import urls as api_urls
from core.views import search

admin.autodiscover()

# Register search signal handlers
wagtailsearch_register_signal_handlers()

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("images/", include(wagtailimages_urls)),
    path("api/", include(api_urls)),
    path("search/", search, name="core_search"),
    path("sitemap.xml", sitemap),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__", include(debug_toolbar.urls)))

    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL + "images/",
        document_root=os.path.join(settings.MEDIA_ROOT, "images"),
    )
else:
    from django.views.static import serve

    urlpatterns.append(
        re_path(
            r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}
        )
    )

urlpatterns.append(
    path("", include(wagtail_urls))
)  # This must always be the last one since it's a catch all.

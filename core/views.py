# views.py

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from wagtail.models import Page
from wagtail.search.models import Query


def search(request):
    # Search
    search_query = request.GET.get("q", None)
    page = request.GET.get("page", 1)

    if search_query:
        search_results = Page.objects.live().search(search_query)

        # Log the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    # Render template
    return render(
        request,
        "core/search_results.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )

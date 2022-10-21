from django.conf import settings


def google_credentials(request):

    return {
        "GOOGLE_ANALYTICS_KEY": getattr(settings, "GOOGLE_ANALYTICS_KEY", False),
        "GOOGLE_TAG_MANAGER": getattr(settings, "GOOGLE_TAG_MANAGER", False),
        "GOOGLE_MAPS_API_KEY": getattr(settings, "GOOGLE_MAPS_API_KEY", False),
    }


def baseurl(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
        scheme = "https://"
    else:
        scheme = "http://"

    return {"BASE_URL": scheme + request.get_host()}


def api_companies_endpoint(request):
    """
    Return a URL to get the JSON of the existing companies
    """
    if settings.DEBUG:
        url = "/api/data.json"
    else:
        url = "/api/companies/?format=json"

    return {"API_COMPANIES_ENDPOINT": url}

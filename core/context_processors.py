from django.conf import settings


def google_analytics(request):
    """
    Use the variables returned in this function to
    render your Google Analytics tracking code template.
    """
    ga_key = getattr(settings, 'GOOGLE_ANALYTICS_KEY', False)
    ga_tag = getattr(settings, 'GOOGLE_TAG_MANAGER', False)
    gak = getattr(settings, 'GOOGLE_API_KEY', False)

    if ga_key:
        return {
            'GOOGLE_ANALYTICS_KEY': ga_key,
            'GOOGLE_TAG_MANAGER': ga_tag,
            'GOOGLE_API_KEY': gak,
        }

    return {}


def baseurl(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    return {'BASE_URL': scheme + request.get_host()}


def api_companies_endpoint(request):
    """
    Return a URL to get the JSON of the existing companies
    """
    if settings.DEBUG:
        url = '/api/data.json'
    else:
        url = '/api/companies/?format=json'

    return {'API_COMPANIES_ENDPOINT': url}

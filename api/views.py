from rest_framework import viewsets

from api.serializers import CompanySerializer
from core.models import WagtailCompanyPage


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows companies to be viewed.
    """

    queryset = (
        WagtailCompanyPage.objects.live()
        .filter(show_map=True)
        .order_by("-first_published_at")
    )
    serializer_class = CompanySerializer
    paginate_by = None

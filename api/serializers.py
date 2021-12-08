from rest_framework import serializers

from core.models import WagtailCompanyPage


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WagtailCompanyPage
        fields = ("title", "lat", "lon", "location", "children_count", "url")

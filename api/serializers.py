from core.models import WagtailCompanyPage
from rest_framework import serializers


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WagtailCompanyPage
        fields = ('title', 'lat', 'lon', 'location', 'children_count', 'url')

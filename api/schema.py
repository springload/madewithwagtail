import graphene

from graphene import relay, List, ObjectType
from graphene_django import DjangoObjectType

from core.models import WagtailCompanyPage


class WagtailCompanyPageNode(DjangoObjectType):
    class Meta:
        model = WagtailCompanyPage
        interfaces = (relay.Node, )


class Query(ObjectType):
    company_pages = List(WagtailCompanyPageNode)

    @graphene.resolve_only_args
    def resolve_company_pages(self):
        return WagtailCompanyPage.objects.live()


schema = graphene.Schema(query=Query)

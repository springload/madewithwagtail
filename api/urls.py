from django.conf import settings
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

from rest_framework import routers

from api.views import CompanyViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    url(r'^graphql', csrf_exempt(GraphQLView.as_view())),
    url(r'^graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True, pretty=True))),
    url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    from django.views.generic import TemplateView
    urlpatterns += [
        url('^data\.json$', TemplateView.as_view(template_name='fixtures/data.json', content_type='text/json')),
    ]

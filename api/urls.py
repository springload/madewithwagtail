from django.conf import settings
from django.conf.urls import url, include

from rest_framework import routers

from api.views import CompanyViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    from django.views.generic import TemplateView
    urlpatterns += [
        url('^data\.json$', TemplateView.as_view(template_name='fixtures/data.json', content_type='text/json')),
    ]

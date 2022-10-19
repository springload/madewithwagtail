from rest_framework import routers

from django.conf import settings
from django.urls import include, path

from api.views import CompanyViewSet

router = routers.DefaultRouter()
router.register(r"companies", CompanyViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    from django.views.generic import TemplateView

    urlpatterns += [
        path(
            "data.json",
            TemplateView.as_view(
                template_name="fixtures/data.json", content_type="text/json"
            ),
        ),
    ]

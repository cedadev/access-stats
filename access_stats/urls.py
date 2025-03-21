from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings

from access_stats.views import IndexView


def health_view(request):
    return HttpResponse("OK")


if settings.PUBLIC_SITE:
    urlpatterns = [
        path("health/", health_view, name="health"),
        path("", include("downloads.urls"))
    ]
else:
    urlpatterns = [
        path("", IndexView.as_view(), name="index"),
        path("downloads/", include("downloads.urls")),
        path("deposits/", include("deposits.urls")),
        path("health/", health_view, name="health"),
    ]

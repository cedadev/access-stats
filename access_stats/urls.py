from django.urls import path, include
from django.conf import settings

from access_stats.views import IndexView

if settings.PUBLIC_SITE:
    urlpatterns = [
        path("", include("downloads.urls"))
    ]
else:
    urlpatterns = [
        path("", IndexView.as_view(), name="index"),
        path("downloads/", include("downloads.urls")),
        path("deposits/", include("deposits.urls")),
    ]

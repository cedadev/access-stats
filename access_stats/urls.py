from django.urls import path, include

from access_stats.views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("downloads/", include("downloads.urls")),
    path("deposits/", include("deposits.urls")),
]

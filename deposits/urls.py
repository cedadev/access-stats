from django.urls import path

from deposits.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]

from django.urls import path

from deposits.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='deposits'),
]
#TODO: ADD JSON, CSV and XLSX VIEWS FROM TOP LEVEL PACKAGE
from django.urls import path

from deposits.views import IndexView, JsonView, TxtView, CsvView, XlsxView

urlpatterns = [
    path("", IndexView.as_view(), name="deposits"),
    path("json/<analysis_method>", JsonView.as_view(), name="deposits/json"),
    path("txt/<analysis_method>", TxtView.as_view(), name="deposits/txt"),
    path("csv/<analysis_method>", CsvView.as_view(), name="deposits/csv"),
    path("xlsx/<analysis_method>", XlsxView.as_view(), name="deposits/xlsx"),
]
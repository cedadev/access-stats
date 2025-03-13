from django.urls import path

from downloads.views import IndexView, JsonView, TxtView, CsvView, XlsxView

urlpatterns = [
    path("", IndexView.as_view(), name="downloads"),
    path("json/<analysis_method>", JsonView.as_view(), name="downloads_json"),
    path("txt/<analysis_method>", TxtView.as_view(), name="downloads_txt"),
    path("csv/<analysis_method>", CsvView.as_view(), name="downloads_csv"),
    path("xlsx/<analysis_method>", XlsxView.as_view(), name="downloads_xlsx"),
]

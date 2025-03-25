from django.urls import path

from obsolete_deposits.views import IndexView, JsonView, TxtView, CsvView, XlsxView

urlpatterns = [
    path("", IndexView.as_view(), name="deposits"),
    path("json/<analysis_method>", JsonView.as_view(), name="deposits_json"),
    path("txt/<analysis_method>", TxtView.as_view(), name="deposits_txt"),
    path("csv/<analysis_method>", CsvView.as_view(), name="deposits_csv"),
    path("xlsx/<analysis_method>", XlsxView.as_view(), name="deposits_xlsx"),
]

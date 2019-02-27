from django.urls import path

from downloads.views import IndexView, JsonView, TxtView, CsvView, XlsxView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('json/<analysis_method>', JsonView.as_view(), name='json'),
    path('txt/<analysis_method>', TxtView.as_view(), name='txt'),
    path('csv/<analysis_method>', CsvView.as_view(), name='csv'),
    path('xlsx/<analysis_method>', XlsxView.as_view(), name='xlsx'),
]

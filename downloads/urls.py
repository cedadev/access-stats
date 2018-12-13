from django.urls import path

from .views import IndexView, JsonView, TxtView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('json/<analysis_method>', JsonView.as_view(), name='json'),
    path('txt/<analysis_method>', TxtView.as_view(), name='txt'),
]

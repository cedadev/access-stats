from django.urls import path

from .views import IndexView, JsonView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('json/<analysis_method>', JsonView.as_view(), name='json'),
]

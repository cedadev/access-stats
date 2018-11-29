from django.urls import path

from .views import IndexView

urlpatterns = [
    path('<analysis_method>/', IndexView.as_view(), name='index'),
    path('', IndexView.as_view(), name='index'),
]

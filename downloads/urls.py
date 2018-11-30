from django.urls import path

from .views import IndexView, JsonView

urlpatterns = [
    path('<analysis_method>/', IndexView.as_view(), name='index'),
    path('', IndexView.as_view(), name='index'),
    path('<analysis_method>/json/', JsonView.as_view(), name='json'),
]

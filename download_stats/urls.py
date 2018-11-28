from django.urls import path, include

urlpatterns = [
    path('downloads/', include('downloads.urls')),
]

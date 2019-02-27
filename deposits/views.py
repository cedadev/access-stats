from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView

default_404_response = HttpResponseNotFound('<h1>404 - Not found</h1>')

class IndexView(TemplateView):
    template_name = "deposits/index.html"
    
    def get(self, request):
        return render(request, self.template_name)

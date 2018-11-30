from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.generic import TemplateView

from .forms import FilterForm
from .query import QueryElasticSearch

valid_analysis_methods = ["methods","timeline","dataset","users","user","trace"]

default_404_response = HttpResponseNotFound('<h1>404 - Not found</h1>')

class IndexView(TemplateView):
    template_name = "downloads/index.html"
    
    def get(self, request, analysis_method="methods"):
        if analysis_method not in valid_analysis_methods:
            return default_404_response
        form = FilterForm(request.GET)
        return render(request, self.template_name, {'form': form, 'analysis_method':analysis_method})

class JsonView(TemplateView):
    def get_data_from_es(self, request, analysis_method):
        return QueryElasticSearch().get_data(request.GET, analysis_method)

    def get(self, request, analysis_method):
        if analysis_method not in valid_analysis_methods:
            return default_404_response
        return JsonResponse(self.get_data_from_es(request, analysis_method))

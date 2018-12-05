from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.generic import TemplateView

from .forms import FilterForm
from .query import QueryElasticSearch

valid_analysis_methods = ["methods","timeline","dataset","user","users","trace"]

default_404_response = HttpResponseNotFound('<h1>404 - Not found</h1>')

class IndexView(TemplateView):
    template_name = "downloads/index.html"
    
    def get(self, request):
        form = FilterForm(request.GET)
        return render(request, self.template_name, {'form': form})

class JsonView(TemplateView):
    def get_data_from_es(self, filters, analysis_method):
        return QueryElasticSearch().get_data(filters, analysis_method)

    def get(self, request, analysis_method):
        form = FilterForm(request.GET)
        if analysis_method not in valid_analysis_methods or not form.is_valid():
            return default_404_response
        return JsonResponse(self.get_data_from_es(form.cleaned_data, analysis_method), json_dumps_params={'indent': 2})

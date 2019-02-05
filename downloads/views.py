from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.generic import TemplateView

from .forms import FilterForm
from .query import QueryElasticSearch

valid_analysis_methods = ["methods","timeline","dataset","dataset-limited","user","users","users-limited","trace"]

default_404_response = HttpResponseNotFound('<h1>404 - Not found</h1>')

class IndexView(TemplateView):
    template_name = "downloads/index.html"
    
    def get(self, request):
        if request.GET:
            form = FilterForm(request.GET)
        else:
            form = FilterForm()
        
        return render(request, self.template_name, {'form': form})

class JsonView(TemplateView):
    def get_data_from_es(self, filters, analysis_method):
        return QueryElasticSearch().get_data(filters, analysis_method)

    def get(self, request, analysis_method):
        form = FilterForm(request.GET)
        if analysis_method not in valid_analysis_methods or not form.is_valid():
            return default_404_response
        return JsonResponse(self.get_data_from_es(form.cleaned_data, analysis_method), json_dumps_params={'indent': 2})

class TxtView(TemplateView):
    def generate_text_file(self, filters, analysis_method):
        json_data = QueryElasticSearch().get_data(filters, analysis_method)
        logs = ""
        for log in json_data["logs"]:
            logs += f"{log}\n"
        return logs

    def get(self, request, analysis_method):
        form = FilterForm(request.GET)
        if analysis_method != "trace" or not form.is_valid():
            return default_404_response
        return HttpResponse(self.generate_text_file(form.cleaned_data, analysis_method), content_type="text/plain")

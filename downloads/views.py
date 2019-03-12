from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.generic import TemplateView

from downloads.forms import FilterForm

from common.json_maker_factory import JsonMakerFactory
from common.file_response_factory import FileResponseFactory

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
    def get(self, request, analysis_method):
        form = FilterForm(request.GET)
        if analysis_method not in ["methods", "timeline", "dataset",
                          "dataset-limited", "user", "users", "users-limited", "trace"] or not form.is_valid():
            return default_404_response
        return JsonResponse(JsonMakerFactory().get(form.cleaned_data, analysis_method).json(), json_dumps_params={'indent': 2})

class TxtView(TemplateView):
    def generate_text_file(self, filters, analysis_method):
        json_data = JsonMakerFactory().get(filters, analysis_method).json()
        logs = ""
        for log in json_data["logs"]:
            logs += f"{log}\n"
        return logs

    def get(self, request, analysis_method):
        form = FilterForm(request.GET)
        if analysis_method != "trace" or not form.is_valid():
            return default_404_response
        return HttpResponse(self.generate_text_file(form.cleaned_data, analysis_method), content_type="text/plain")

class CsvView(TemplateView):
    def get(self, request, analysis_method):
        form = FilterForm(request.GET)
        if analysis_method not in ["methods", "timeline", "dataset", "users"] or not form.is_valid():
            return default_404_response

        return FileResponseFactory().get(form.cleaned_data, analysis_method).make_csv()

class XlsxView(TemplateView):
    def get(self, request, analysis_method):
        form = FilterForm(request.GET)
        if analysis_method not in ["methods", "timeline", "dataset", "users"] or not form.is_valid():
            return default_404_response

        return FileResponseFactory().get(form.cleaned_data, analysis_method).make_xlsx()

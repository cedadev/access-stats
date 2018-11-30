from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.generic import TemplateView

from .forms import FilterForm

valid_analysis_methods = ["methods","timeline","dataset","users","user","trace"]

class IndexView(TemplateView):
    template_name = "downloads/index.html"
    
    def get(self, request, analysis_method="methods"):
        if analysis_method not in valid_analysis_methods:
            return HttpResponseNotFound('<h1>404 - Not found</h1>')
        form = FilterForm(request.GET)
        return render(request, self.template_name, {'form': form, 'analysis_method':analysis_method})

class JsonView(TemplateView):
    def make_data(self, request, analysis_method):
        return {analysis_method:request.GET.get("start","none")}

    def get(self, request, analysis_method):
        if analysis_method not in valid_analysis_methods:
            return HttpResponseNotFound('<h1>404 - Not found</h1>')
        return JsonResponse(self.make_data(request, analysis_method))

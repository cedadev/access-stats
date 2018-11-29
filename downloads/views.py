from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import TemplateView

from .forms import FilterForm

class IndexView(TemplateView):
    template_name = "downloads/index.html"
    analysis_methods = ["methods","timeline","dataset","users","user","trace"]

    def get(self, request, analysis_method="methods"):
        if analysis_method not in self.analysis_methods:
            return HttpResponseNotFound('<h1>404 - Not found</h1>')
        form = FilterForm(request.GET)
        return render(request, self.template_name, {'form': form, 'analysis_method':analysis_method})

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import FilterForm

def index(request):
    if request.method == "GET":
        form = FilterForm(request.GET)
    return render(request, "downloads/index.html", {'form': form})

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    var = True
    template = loader.get_template("downloads/index.html")
    context = {"var" : var}
    return HttpResponse(template.render(context, request))

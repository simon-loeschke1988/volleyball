from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse

# Create your views here.

def index(request):
    # index.html is located in applikation/webapp/templates/index.html, but we don't need to specify the full path // Simon Löschke
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


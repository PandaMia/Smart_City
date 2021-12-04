# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Pothole
from django.core import serializers
import os
import mimetypes

def index(request):
    context = {'segment': 'index'}
    porholes = Pothole.objects.all().order_by('-value')
    json_serializer = serializers.get_serializer("json")()
    companies = json_serializer.serialize(Pothole.objects.all().order_by('-value'), ensure_ascii=False)
    context['porholes'] = porholes
    context['companies'] = companies
    context['danger'] = len(Pothole.objects.filter(value__gte=0.9))
    context['warning'] = len(Pothole.objects.filter(value__gte=0.5)) - len(Pothole.objects.filter(value__gte=0.9))
    context['normaly'] = len(Pothole.objects.filter(value__lt=0.5))
    context['test'] = 'test'
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        #if 'cam_id' in request:
        if request.GET.get("cam_id"):
            porhole = Pothole.objects.get(pId=request.GET.get("cam_id"))
            context['porhole'] = porhole
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def downloadfile(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'simple_demo.pdf'
    path = os.path.join(
        BASE_DIR,
        filename
    )
    filename = os.path.basename(path)
    # Open the file for reading content
    path = open(filename, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filename)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response

def downloadfileheat(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'heatmap.result.jpg'
    path = os.path.join(
        BASE_DIR,
        filename
    )
    filename = os.path.basename(path)
    # Open the file for reading content
    path = open(filename, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filename)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response
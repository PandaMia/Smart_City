# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf.urls.static import static
from django.conf import settings
from apps.home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('downloadfile', views.downloadfile, name='downloadfile'),
    path('downloadfileheat', views.downloadfileheat, name='downloadfileheat'),
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.home.urls")),            # UI Kits Html files
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

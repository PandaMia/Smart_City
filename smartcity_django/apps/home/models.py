# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Pothole(models.Model):
    pId = models.PositiveIntegerField()
    cameraUrl = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    video = models.FileField(upload_to='home', null=True,
                             validators=[
                                 FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    value = models.FloatField(default=.0)
    longitude = models.FloatField(default=.0)
    latitude = models.FloatField(default=.0)
    img = models.ImageField(upload_to='home', null=True, blank = True)


    @classmethod
    def create(cls, _id, _url, _address, _val, _long, _lat):
        return cls(pId=_id, cameraUrl=_url, address=_address, value=_val, longitude=_long, latitude=_lat)

    def __str__(self):
        return f'({str(self.pId)}) {self.cameraUrl}: {self.value}'

# Create your models here.


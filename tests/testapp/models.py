# -*- coding: utf-8 -*-
"""
Created on July 11, 2016

@author: bwawok@gmail.com
"""

from django.db import models


class FirstModel(models.Model):
    age = models.IntegerField()
    name = models.TextField(max_length=100)
    color = models.TextField(max_length=100)


class SecondModel(models.Model):
    age = models.IntegerField()
    name = models.TextField(max_length=100)
    size = models.IntegerField()


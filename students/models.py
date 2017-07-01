# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Students(models.Model):
    name = models.CharField(max_length=200)
    roll = models.CharField(max_length=20, primary_key=True)
    room = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=12)
    password = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Students'

    def __unicode__(self):
        return str(self.name) + ' - ' + str(self.roll)

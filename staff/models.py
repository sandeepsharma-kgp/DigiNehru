# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Permission(models.Model):
    api_name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Permission'

    def __unicode__(self):
        return str(self.name) + ' - ' + str(self.empid)


class Role(models.Model):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission)

    class Meta:
        verbose_name_plural = 'Role'

    def __unicode__(self):
        return str(self.name) + ' - ' + str(self.empid)


class Staff(models.Model):
    name = models.CharField(max_length=200)
    empid = models.CharField(max_length=20, primary_key=True)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=12)
    password = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    role = models.ForeignKey(Role, default=4)

    class Meta:
        verbose_name_plural = 'Staff'

    def __unicode__(self):
        return str(self.name) + ' - ' + str(self.empid)

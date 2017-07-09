# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from food.utils import get_all_fields
# Create your models here.


class Students(models.Model):
    name = models.CharField(max_length=200)
    roll = models.CharField(max_length=20, primary_key=True)
    room = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=12)
    password = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    token = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Students'

    def __unicode__(self):
        return str(self.name) + ' - ' + str(self.roll)

    def serializer(self):
        data = {}
        field_list = get_all_fields(self._meta.fields,
                                    self._meta.many_to_many)
        for field in field_list:
            if not field.name == 'password' \
                    and not field.name == 'status':
                data[field.name] = getattr(self, field.name)
        return data

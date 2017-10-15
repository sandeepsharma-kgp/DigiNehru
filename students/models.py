# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from food.utils import get_all_fields
from .constants import ACTIVE, INACTIVE
# Create your models here.


class Base(models.Model):

    STATUS_CHOICE = ((ACTIVE, 'Active'),
                     (INACTIVE, 'Inactive')
                     )

    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)
    status = models.SmallIntegerField(default=INACTIVE,
                                      choices=STATUS_CHOICE)

    class Meta:
        abstract = True


class Students(Base):
    name = models.CharField(max_length=200, blank=True, null=True)
    roll = models.CharField(max_length=20, primary_key=True)
    room = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    mobile = models.CharField(max_length=12, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    token = models.CharField(max_length=200, blank=True, null=True)
    profile = models.URLField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Students'
        unique_together = ('roll', 'token')

    def __unicode__(self):
        return str(self.name) + ' - ' + str(self.roll) + ' - ' + str(self.created_on.date())

    def serializer(self):
        data = {}
        field_list = get_all_fields(self._meta.fields,
                                    self._meta.many_to_many)
        for field in field_list:
            if not field.name == 'password' \
                    and not field.name == 'status':
                data[field.name] = getattr(self, field.name)
        return data

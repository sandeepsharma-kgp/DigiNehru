# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .constants import METHOD_CHOICES, GET
from multiselectfield import MultiSelectField
from DigiNehruPy.utils import get_all_fields

# Create your models here.


class Base(models.Model):
    ACTIVE = 0
    INACTIVE = 1

    STATUS_CHOICE = ((ACTIVE, 'Active'),
                     (INACTIVE, 'Inactive')
                     )

    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)
    status = models.SmallIntegerField(default=ACTIVE,
                                      choices=STATUS_CHOICE)

    class Meta:
        abstract = True


class Permission(Base):
    api_name = models.CharField(max_length=200)
    method = MultiSelectField(
        max_choices=4, choices=METHOD_CHOICES, default=GET)

    class Meta:
        verbose_name_plural = 'Permission'

    def __unicode__(self):
        return str(self.api_name) + ' - ' + str(self.method)


class Role(Base):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission)

    class Meta:
        verbose_name_plural = 'Role'

    def __unicode__(self):
        return str(self.name) + ' - ' + str(self.permissions)


class Staff(Base):
    name = models.CharField(max_length=200)
    empid = models.CharField(max_length=20, primary_key=True)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=12)
    password = models.CharField(max_length=200)
    role = models.ForeignKey(Role, default=1)
    profile = models.URLField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Staff'

    def __unicode__(self):
        return str(self.name) + ' - ' + str(self.empid)

    def serializer(self):
        data = {}
        field_list = get_all_fields(self._meta.fields,
                                    self._meta.many_to_many)
        for field in field_list:
            if not field.name == 'password' and not field.name == 'status':
                data[field.name] = getattr(self, field.name)
                if field.many_to_one:
                    data[field.name] = getattr(self, field.name).name
        return data

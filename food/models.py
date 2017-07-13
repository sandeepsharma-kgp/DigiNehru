# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from multiselectfield import MultiSelectField
from .constants import (DAY_CHOICES, TIME_CHOICES,
                        VN_CHOICES, MON, BREAKFAST,
                        VEG)
from .utils import get_all_fields
from datetime import datetime
from DigiNehruPy.utils import convert_date
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


class FoodType(Base):
    type_name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return str(self.type_name)

    # def serializer(self, m2m=False):
    #     data = {}
    #     field_list = get_all_fields(self._meta.fields,
    #                                 self._meta.many_to_many)
    #     for field in field_list:
    #         data[field.name] = getattr(self, field.name)

    #     return data


class FoodItem(Base):
    food_name = models.CharField(max_length=100, unique=True)
    type_name = models.ForeignKey(FoodType, on_delete=models.CASCADE)
    vn = MultiSelectField(choices=VN_CHOICES, max_choices=2, default=VEG)

    def __unicode__(self):
        return str(self.food_name)

    def serializer(self, m2m=False, vn=None):
        data = {}
        field_list = get_all_fields(self._meta.fields,
                                    self._meta.many_to_many)
        if not vn or vn in self.vn and self.status:
            for field in field_list:
                if field.many_to_one:
                    data[field.name] = {getattr(self, field.name).id: getattr(
                        self, field.name).type_name}
                elif field.many_to_many:
                    m2m_list = []
                    if m2m:
                        m2m_list = [obj.serializer()
                                    for obj in getattr(self, field.name).all()]
                        data[field.name] = m2m_list
                else:
                    if isinstance(getattr(self, field.name), datetime):
                        data[field.name] = convert_date(
                            getattr(self, field.name), '%Y-%m-%d %H:%M:%S')
                    else:
                        data[field.name] = getattr(self, field.name)

        # here goes properties
        return data


class Menu(Base):
    day = models.PositiveIntegerField(
        choices=DAY_CHOICES, default=MON)
    time = models.PositiveIntegerField(
        choices=TIME_CHOICES, default=BREAKFAST)
    food_item = models.ManyToManyField(FoodItem)

    def __unicode__(self):
        return str(self.get_day_display()) + ' - ' + str(self.
                                                         get_time_display())

    class Meta:
        unique_together = ("day", "time")

    def serializer(self, m2m=False, vn=None):
        data = {}
        field_list = get_all_fields(self._meta.fields,
                                    self._meta.many_to_many)

        for field in field_list:
            data[field.name] = getattr(self, field.name)
            if field.many_to_one:
                data[field.name] = getattr(self, field.name + '_id')
            elif field.many_to_many:
                m2m_list = []
                if m2m:
                    for obj in getattr(self, field.name).all():
                        fi = obj.serializer(vn=vn)
                        if fi:
                            m2m_list.append(fi)
                    data[field.name] = m2m_list
        # here goes properties
        return data

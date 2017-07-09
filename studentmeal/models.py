# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_mysql.models import JSONField, Model
from students.models import Students
from food.models import Menu
from food.constants import TIME_CHOICES, VN_CHOICES
from multiselectfield import MultiSelectField
from DigiNehruPy.utils import get_all_fields
# Create your models here.


class eating(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    eating_on = models.DateField()
    eating_item = JSONField()
    meals_opted = MultiSelectField(
        choices=TIME_CHOICES, max_choices=4, default=list())
    meals_taken = MultiSelectField(
        choices=TIME_CHOICES, max_choices=4, default=list())

    def __unicode__(self):
        return str(self.student) + ' - ' + str(self.eating_on)

    class Meta:
        unique_together = ('student', 'eating_on')

    def serializer(self, m2m=False):
        data = {}
        field_list = get_all_fields(self._meta.fields,
                                    self._meta.many_to_many)

        for field in field_list:
            data[field.name] = getattr(self, field.name)
            if field.many_to_one:
                st = getattr(self, field.name)
                data[field.name] = [st.name, st.roll]
        # here goes properties
        return data

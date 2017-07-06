# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_mysql.models import JSONField, Model
from students.models import Students
from food.models import Menu
from food.constants import TIME_CHOICES, VN_CHOICES
from multiselectfield import MultiSelectField
# Create your models here.


class eating(models.Model):
    student_roll = models.ForeignKey(Students, on_delete=models.CASCADE)
    eating_on = models.DateField()
    eating_item = JSONField()
    meals_taken = MultiSelectField(
        choices=TIME_CHOICES, max_choices=4, default=list())

    def __unicode__(self):
        return str(self.student_roll) + ' - ' + str(self.eating_on)

    class Meta:
        unique_together = ('student_roll', 'eating_on')

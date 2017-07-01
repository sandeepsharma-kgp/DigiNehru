# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from students.models import Students
from food.models import Menu
from food.constants import TIME_CHOICES, VN_CHOICES
# Create your models here.


class eating(models.Model):
    student = models.ForeignKey(Students)
    eating_on = models.DateTimeField()
    eating_time = models.PositiveIntegerField(choices=TIME_CHOICES)
    eating_type = models.CharField(max_length=2, choices=VN_CHOICES)
    eating_item = models.ManyToMany(Menu)
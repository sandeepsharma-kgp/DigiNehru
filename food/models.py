# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from multiselectfield import MultiSelectField
from .constants import DAY_CHOICES, TIME_CHOICES, VN_CHOICES, MON, BREAKFAST

# Create your models here.


class FoodType(models.Model):
    type_name = models.CharField(max_length=100)


class FoodItem(models.Model):
    food_name = models.CharField(max_length=100)
    type_name = models.ForeignKey(FoodType)
    vn = MultiSelectField(choices=VN_CHOICES, max_choices=2)


class Menu(models.Model):
    day = MultiSelectField(
        choices=DAY_CHOICES, default=MON, max_choices=7)
    time = MultiSelectField(
        choices=TIME_CHOICES, default=BREAKFAST, max_choices=4)
    food_item = models.ForeignKey(FoodItem)

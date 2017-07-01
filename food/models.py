# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .constants import DAY_CHOICES, TIME_CHOICES, VN_CHOICES, MON, BREAKFAST

# Create your models here.


class FoodType(models.Model):
    type_name = models.CharField(max_length=100)


class FoodItem(models.Model):
    food_name = models.CharField(max_length=100)
    type_name = models.ForeignKey(FoodType, default=0)
    vn = models.CharField(max_length=2, choices=VN_CHOICES)


class Menu(models.Model):
    day = models.PositiveIntegerField(choices=DAY_CHOICES, default=MON)
    time = models.PositiveIntegerField(choices=TIME_CHOICES, default=BREAKFAST)
    food_item = models.ForeignKey(FoodItem)

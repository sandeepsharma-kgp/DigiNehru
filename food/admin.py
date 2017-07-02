# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import FoodType, Menu, FoodItem
# Register your models here.
admin.site.register(FoodType)
admin.site.register(FoodItem)
admin.site.register(Menu)

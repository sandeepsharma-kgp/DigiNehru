# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import eating, mealcount
# Register your models here.
admin.site.register(eating)
admin.site.register(mealcount)

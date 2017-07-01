# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Students
# Register your models here.


class StudentsAdmin(admin.ModelAdmin):
    search_fields = ['name', 'roll']

admin.site.register(Students, StudentsAdmin)

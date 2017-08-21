# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Staff, Role, Permission
# Register your models here.


class StaffAdmin(admin.ModelAdmin):
    search_fields = ['name', 'empid']

admin.site.register(Staff, StaffAdmin)
admin.site.register(Role)
admin.site.register(Permission)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import FoodItem, FoodType, Menu
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives
from DigiNehruPy.decorator import check_login
from datetime import datetime, timedelta
import pytz
# Create your views here.


def send_200(data):
    return JsonResponse(data=data, status=200)


def send_400(data):
    return JsonResponse(data=data, status=400)


def init_response(res_str=None, data=None):
    response = {}
    response["res_str"] = ""
    response["res_data"] = {}
    if res_str is not None:
        response["res_str"] = res_str
    if data is not None:
        response["res_data"] = data
    return response


def send_email(email):
    from_email = "sandeep@happay.in"
    subject = "Change Password"
    to_email = email
    to = [to_email]
    email_text = "link"
    msg = EmailMultiAlternatives(
        subject, email_text, from_email, to)
    try:
        msg.send()
    except:
        pass


class FoodEntry(View):

    def __init__(self):
        self.response = init_response()

    @check_login
    def post(self, request, *args, **kwargs):
        data = request.POST
        food_name = data['food_name'].lower()
        type_name = data['food_type'].lower()
        vn = data.getlist('vn')
        try:
            type_name = FoodType.objects.get(type_name=type_name)
            FoodItem.objects.create(
                food_name=food_name, type_name=type_name, vn=vn)

            self.response['res_str'] = "Data added"
            return send_200(self.response)
        except Exception as e:
            print e
            self.response['res_str'] = "Data not added"
            return send_400(self.response)

    @check_login
    def get(self, request, *args, **kwargs):
        food_data = FoodItem.objects.all().values_list('pk', 'food_name')
        food_list = {}
        for i in food_data:
            food_list[i[0]] = i[1]
        self.response['res_str'] = "food_list"
        self.response['res_data'] = food_list
        return send_200(self.response)


class FoodTypeName(View):

    def __init__(self):
        self.response = init_response()

    def post(self, request, *args, **kwargs):
        data = request.POST
        type_name = data['type_name'].lower()

        try:
            FoodType.objects.create(type_name=type_name)
            self.response['res_str'] = "Data added"
            return send_200(self.response)
        except Exception as e:
            print e
            self.response['res_str'] = "Data not added"
            return send_400(self.response)

    def get(self, request, *args, **kwargs):
        type_data = FoodType.objects.all().values_list('pk', 'type_name')
        type_list = {}
        for i in type_data:
            type_list[i[0]] = i[1]
        self.response['res_str'] = "type_list"
        self.response['res_data'] = type_list
        return send_200(self.response)


class MenuEntry(View):

    def __init__(self):
        self.response = init_response()

    def post(self, request, *args, **kwargs):
        data = request.POST
        day = data['day']
        time = data['time']
        food_item = data['food_item']
        food_item = food_item.split(",")
        try:
            food_item = FoodItem.objects.filter(pk__in=food_item)
            try:
                menu = Menu.objects.get(day=day, time=time)
            except:
                menu = None
            if not menu:
                menu = Menu.objects.create(
                    day=day, time=time)
                setattr(menu, 'food_item', food_item)
                self.response['res_str'] = "Data added"
                return send_200(self.response)
            else:
                setattr(menu, 'food_item', food_item)
                self.response['res_str'] = "Data added"
                return send_200(self.response)

        except Exception as e:
            print e
            self.response['res_str'] = "Data not added"
            return send_400(self.response)

    def get(self, request, *args, **kwargs):
        data = request.GET
        day = data['day']
        if data['limited']:
            if day == 0:
                day = datetime.now(pytz.utc).weekday()
            else:
                day = (datetime.now(pytz.utc) + timedelta(1)).weekday()
        time = data['time']
        vn = data['vn']
        menu = Menu.objects.all()
        if day:
            menu = menu.filter(day=day)
        if time:
            menu = menu.filter(time=time)
        qs_json = {}

        for qs in menu:
            qs_json[qs.id] = qs.serializer(True, vn)

        self.response['res_str'] = "menu_list"
        self.response['res_data'] = qs_json
        return send_200(self.response)

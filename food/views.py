# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import FoodItem, FoodType, Menu
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives
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

    def post(self, request, *args, **kwargs):
        data = request.POST
        food_name = data['food_name']
        food_type = data['food_type']
        vn = []
        vn.append(data['vn'])

        try:
            FoodItem.objects.create(
                food_name=food_name, food_type=food_type, vn=vn)

            self.response['res_str'] = "Data added"
            return send_200(self.response)
        except Exception as e:
            print e
            self.response['res_str'] = "Data not added"
            return send_400(self.response)


class MenuEntry(View):

    def __init__(self):
        self.response = init_response()

    def post(self, request, *args, **kwargs):
        data = request.POST
        day = []
        time = []
        day.append(data['day'])
        time.append(data['time'])
        food_item = data['food_item']

        try:
            Menu.objects.create(
                day=day, time=time, food_item=food_item)

            self.response['res_str'] = "Data added"
            return send_200(self.response)
        except Exception as e:
            print e
            self.response['res_str'] = "Data not added"
            return send_400(self.response)

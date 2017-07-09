# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives
from food.constants import BREAKFAST, LUNCH, SNACKS, DINNER
from .models import eating
from datetime import datetime
import pytz
from students.models import Students
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


class StudentMenuEntry(View):

    def __init__(self):
        self.response = init_response()

    def post(self, request, *args, **kwargs):
        data = request.POST
        meal = {}
        meal[BREAKFAST] = {}
        meal[LUNCH] = {}
        meal[SNACKS] = {}
        meal[DINNER] = {}
        roll = data['roll']
        meals_opted = []
        # eating_on = data['date']
        import ipdb
        ipdb.set_trace()
        eating_on = datetime.now(pytz.utc).date()

        if data['breakfast']:
            meal[BREAKFAST]['vn'] = data['breakfast_vn']
            meal[BREAKFAST]['menu'] = data.getlist('breakfast')
            meals_opted.append(str(BREAKFAST))
        if data['lunch']:
            meal[LUNCH]['vn'] = data['lunch_vn']
            meal[LUNCH]['menu'] = data.getlist('lunch')
            meals_opted.append(str(LUNCH))
        if data['snacks']:
            meal[SNACKS]['vn'] = data['snacks_vn']
            meal[SNACKS]['menu'] = data.getlist('snacks')
            meals_opted.append(str(SNACKS))
        if data['dinner']:
            meal[DINNER]['vn'] = data['dinner_vn']
            meal[DINNER]['menu'] = data.getlist('dinner')
            meals_opted.append(str(DINNER))

        try:
            roll = Students.objects.get(roll=roll)
            try:
                eat = eating.objects.get(student_roll=roll,
                                         eating_on=eating_on)
            except:
                eat = None

            if eat:
                eat.eating_item = meal
                eat.meals_opted = meals_opted
                eat.save()
                self.response['res_str'] = "Data added"
                return send_200(self.response)
            else:
                eating.objects.create(student=roll, eating_on=eating_on,
                                      eating_item=meal, meals_taken=[],
                                      meals_opted=meals_opted)
                self.response['res_str'] = "Data added"
                return send_200(self.response)
        except Exception as e:
            print e
            self.response['res_str'] = "Data not added"
            return send_400(self.response)

    def get(self, request, *args, **kwargs):
        data = request.GET
        roll = data['roll']
        eat = eating.objects.get(student=roll)
        self.response['res_str'] = "eating_items"
        self.response['res_data'] = eat.serializer()
        return send_200(self.response)

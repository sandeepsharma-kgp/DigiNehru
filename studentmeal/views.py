# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives
from food.constants import BREAKFAST, LUNCH, SNACKS, DINNER
from .models import eating
from datetime import datetime, timedelta
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
        eating_on = data['day']

        if eating_on == 0:
            eating_on = datetime.now(pytz.utc).weekday()
        else:
            eating_on = (datetime.now(pytz.utc) + timedelta(1)).weekday()

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
        eat = eating.objects.filter(student=roll)
        day = data['day']
        if data['limited']:
            if day == 0:
                dated = datetime.now(pytz.utc).weekday()
            else:
                dated = (datetime.now(pytz.utc) + timedelta(1)).weekday()
            eat = eating.objects.filter(eating_on=dated)
        eatings = {}
        for i in eat:
            eatings[str(i.eating_on)] = i.serializer()
        self.response['res_str'] = "eating_items"
        self.response['res_data'] = eatings
        return send_200(self.response)


class StudentMealTaken():

    def __init__(self):
        self.response = init_response()

    def post(self, request, *args, **kwargs):
        data = request.POST
        roll = data['roll']
        dated = data['dated']
        time = data['time']
        try:
            eat = eating.objects.filter(eating_on=dated, student=roll)
        except:
            self.response['res_str'] = \
                "You are not registered for any meal on this day"
            return send_400(self.response)
        if time in eat.meals_opted:
            eat.meals_taken = time
            eat.save()
        else:
            self.response['res_str'] = \
                "You are not registered for this meal on this day"
            return send_400(self.response)

        self.response['res_str'] = "You are good to get your food!"
        return send_200(self.response)


class MealCount():

    def __init__(self):
        self.response = init_response()

    def post(self, request, *args, **kwargs):
        data = request.POST
        roll = data['roll']
        time = data['time']
        # for present day entry
        eating_on = datetime.now(pytz.utc).weekday()

        try:
            roll = Students.objects.get(roll=roll)
            try:
                eat = mealcount.objects.get(student_roll=roll,
                                            eating_on=eating_on)
            except:
                eat = None

            if eat:
                eat.meals_taken = time
                eat.save()
                self.response['res_str'] = "Data added"
                return send_200(self.response)
            else:
                eating.objects.create(student=roll, eating_on=eating_on,
                                      meals_taken=time)
                self.response['res_str'] = "Data added"
                return send_200(self.response)
        except Exception as e:
            print e
            self.response['res_str'] = "Data not added"
            return send_400(self.response)

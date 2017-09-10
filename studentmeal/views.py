# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives
from food.constants import BREAKFAST, LUNCH, SNACKS, DINNER
from .models import eating, mealcount
from datetime import datetime, timedelta
import pytz
from dateutil import tz
from students.models import Students
from students.constants import ACTIVE, INACTIVE
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
                eat = eating.objects.get(student=roll,
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


class MealCount(View):

    def __init__(self):
        self.response = init_response()

    def post(self, request, *args, **kwargs):
        data = request.POST
        if data['d_id'] != 'd03631c7040d29dc':
            self.response['res_str'] = "Wrong Device"
            return send_400(self.response)
        id_ = data['id']
        import ipdb
        ipdb.set_trace()
        # time = data['time']
        time = "-1"
        dated = datetime.now(pytz.utc)
        hr = datetime.strptime(str(dated.astimezone(tz.gettz('Asia/Kolkata'))),
                               '%Y-%m-%d%H:%M:%S.%f+05:30')
        hrs = hr.hour
        if hrs <= 10 and hrs >= 7:
            time = "0"
        elif hrs >= 12 and hrs <= 14:
            time = "1"
        elif hrs >= 16 and hrs <= 18:
            time = "2"
        elif hrs >= 19 and hrs <= 21:
            time = "3"
        vn_choice = data['vn']
        vn = {}
        vn[time] = vn_choice
        if time not in ["0", "1", "2", "3"]:
            self.response['res_str'] = "You are late! Mess is closed!!"
            return send_400(self.response)
        # for present day entry
        eating_on = datetime.now(pytz.utc).date()
        try:
            st = Students.objects.get(token=id_)
            if st.status == INACTIVE:
                self.response['res_str'] = "Account has been purged!!\
                                            \nContact: diginehru@gmail.com"
                return send_400(self.response)
            try:
                eat = mealcount.objects.get(student=st,
                                            eating_on=eating_on)
            except:
                eat = None

            if eat:
                if time in eat.meals_taken:
                    self.response['res_str'] = "Meal already taken!!"
                    return send_400(self.response)
                eat.meals_taken.append(time)
                eat.vn[time] = vn_choice
                eat.save()
                self.response['res_str'] = "You can take your meal"
                return send_200(self.response)
            else:
                mealcount.objects.create(student=st, eating_on=eating_on,
                                         meals_taken=time, vn=vn)
                self.response['res_str'] = "You can take your meal"
                return send_200(self.response)
        except Exception as e:
            print e
            self.response['res_str'] = "Invalid Detail"
            return send_400(self.response)

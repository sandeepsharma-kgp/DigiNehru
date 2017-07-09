# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Students
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives
import uuid
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


class StudentSignUp(View):

    def __init__(self):
        self.response = init_response()

    def update(self, data, st):
        name = data['name']
        roll = data['roll']
        room = data['room']
        email = data['email']
        mobile = data['mobile']
        password = data['password']

        st.name = name
        st.roll = roll
        st.room = room
        st.email = email
        st.mobile = mobile
        st.password = password

        st.save()

    def post(self, request, *args, **kwargs):
        data = request.POST
        name = data['name']
        roll = data['roll']
        room = data['room']
        email = data['email']
        mobile = data['mobile']
        password = data['password']

        st = None

        try:
            st = Students.objects.get(roll=roll)
        except:
            pass

        if st and not st.status:
            self.update(data, st)

        try:
            if not st:
                Students.objects.create(
                    name=name, roll=roll, room=room,
                    email=email, mobile=mobile,
                    password=password)
            else:
                raise Exception('Student already registered')
            self.response['res_str'] = "Data added"
            return send_200(self.response)
        except Exception as e:
            print e
            self.response['res_str'] = "Data not added"
            return send_400(self.response)


class StudentLogin(View):

    def __init__(self):
        self.response = init_response()

    def post(self, request, *args, **kwargs):
        data = request.POST
        roll = data['roll']
        password = data['password']

        try:
            st = Students.objects.get(roll=roll, password=password)
        except:
            st = None
        if st:
            st.token = uuid.uuid1()
            st.save()
            self.response['res_str'] = "student-detail"
            self.response['res_data'] = st.serializer()
            return send_200(self.response)
        else:
            self.response['res_str'] = "student not exist"
            return send_400(self.response)


class ForgotPassword(View):

    def get(self, request, *args, **kwargs):
        data = request.GET
        roll = data['roll']

        st = Students.objects.get(roll=roll)

        email = st.email

        send_email(email)

        self.response['res_str'] = "Link sent"
        return send_200(self.response)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Staff
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives
import uuid
from DigiNehruPy.utils import setex
from DigiNehruPy.decorator import check_login
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


class StaffSignUp(View):

    def __init__(self):
        self.response = init_response()

    def post(self, request, *args, **kwargs):
        data = request.POST
        name = data['name']
        empid = data['empid']
        email = data['email']
        mobile = data['mobile']
        password = data['password']

        st = None
        try:
            st = Staff.objects.get(name=name, empid=empid, email=email)
        except:
            pass

        try:
            if not st:
                Staff.objects.create(
                    name=name, empid=empid, email=email, mobile=mobile,
                    password=password)
            else:
                raise Exception('Staff already registered')
            self.response['res_str'] = "Data added"
            return send_200(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            return send_400(self.response)


class StaffLogin(View):

    def __init__(self):
        self.response = init_response()

    def post(self, request, *args, **kwargs):
        data = request.POST
        empid = data['empid']
        password = data['password']
        import ipdb
        ipdb.set_trace()

        try:
            st = Staff.objects.get(empid=empid, password=password)
        except:
            st = None
        if st:
            # st.token = uuid.uuid1()
            # st.save()
            token = uuid.uuid1()
            setex(st.empid, token, 900)
            self.response['res_str'] = "staff-detail"
            self.response['res_data'] = st.serializer()
            self.response['token'] = token
            return send_200(self.response)
        else:
            self.response['res_str'] = "staff not exist"
            return send_400(self.response)


class ForgotPassword(View):

    def get(self, request, *args, **kwargs):
        data = request.GET
        empid = data['empid']
        password = data['password']

        st = Staff.objects.get(empid=empid)

        st.password = password
        st.save()

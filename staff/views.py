# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Staff
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives, get_connection
import uuid
from DigiNehruPy.utils import setex
from DigiNehruPy.decorator import check_login
from DigiNehruPy.settings import (EMAIL_HOST, EMAIL_HOST_USER,
                                  EMAIL_HOST_PASSWORD,
                                  AWS_ACCESS_KEY_ID,
                                  AWS_SECRET_ACCESS_KEY,
                                  AWS_STORAGE_BUCKET_NAME,
                                  REGION_HOST)
from DigiNehruPy.server_config import PROJECT_PATH
from DigiNehruPy.server_config import  S3_BUCKET
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import os
IMAGE_PATH = PROJECT_PATH + 'PROFILE_IMAGES/'
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


def send_error_email(error_msg):
    connection = get_connection(username=EMAIL_HOST_USER,
                                password=EMAIL_HOST_PASSWORD,
                                fail_silently=False)

    from_email = "diginehru@gmail.com"
    subject = "Error"
    to_email = from_email
    to = [to_email]
    email_text = error_msg
    message_arr = []
    msg = EmailMultiAlternatives(
        subject, email_text, from_email, to)
    message_arr.append(msg)
    try:
        connection.open()
        connection.send_messages(message_arr)
        connection.close()
    except Exception as e:
        print e


def send_email(email, password):
    connection = get_connection(username=EMAIL_HOST_USER,
                                password=EMAIL_HOST_PASSWORD,
                                fail_silently=False)

    from_email = "diginehru@gmail.com"
    subject = "Change Password"
    to_email = email
    to = [to_email]
    email_text = password
    message_arr = []
    msg = EmailMultiAlternatives(
        subject, email_text, from_email, to)
    message_arr.append(msg)
    try:
        connection.open()
        connection.send_messages(message_arr)
        connection.close()
    except Exception as e:
        print e


def copy_contents_to_s3_public(s3_file_name, file_path):
    conn = S3Connection(AWS_ACCESS_KEY_ID,
                        AWS_SECRET_ACCESS_KEY, host=REGION_HOST)
    bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
    k = Key(bucket)
    k.key = s3_file_name
    k.set_contents_from_filename(file_path)
    k.set_acl('public-read')
    k.close()
    s3_link = S3_BUCKET + s3_file_name
    return s3_link


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
        profile = request.FILES['profile']

        st = None
        try:
            st = Staff.objects.get(name=name, empid=empid, email=email)
        except:
            pass

        try:
            if not st:
                print "in generate image url"
                if not os.path.exists(IMAGE_PATH):
                    os.makedirs(IMAGE_PATH)
                    os.chmod(IMAGE_PATH, 0777)
                image_src = IMAGE_PATH + empid + '.png'
                f = open(image_src, 'w')
                f.write(profile.read())
                f.close()
                s3_path = 'profileimages/' + empid
                s3_link = copy_contents_to_s3_public(s3_path, image_src)
                Staff.objects.create(name=name, empid=empid,
                                     email=email, mobile=mobile,
                                     password=password, profile=s3_link)
            else:
                raise Exception('Staff already registered')
            self.response['res_str'] = "Data added"
            return send_200(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
            import traceback
            send_error_email(traceback.format_exc())
            return send_400(self.response)


class StaffLogin(View):

    def __init__(self):
        self.response = init_response()

    def post(self, request, *args, **kwargs):
        data = request.POST
        empid = data['empid']
        password = data['password']
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

        st = Staff.objects.get(empid=empid)

        password = "123456"
        st.password = password
        st.save()

        email = "diginehru@happay.in"

        send_email(email, password)

        self.response['res_str'] = "Link sent"
        return send_200(self.response)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render
from .models import Students
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives, get_connection
import uuid
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
from tasks import add
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


def send_email(email, password):
    connection = get_connection(username=EMAIL_HOST_USER,
                                password=EMAIL_HOST_PASSWORD,
                                fail_silently=False)

    from_email = "sandeepsharma.iit@gmail.in"
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
        file = request.FILES
        name = data['name']
        roll = data['roll']
        room = data['room']
        email = data['email']
        mobile = data['mobile']
        password = data['password']
        profile = file['profile']
        add.apply_async(args=[])

        st = None
        try:
            st = Students.objects.get(roll=roll)
        except:
            pass

        if st and not st.status:
            self.update(data, st)
        try:
            if not st:
                print "in generate image url"
                if not os.path.exists(IMAGE_PATH):
                    os.makedirs(IMAGE_PATH)
                    os.chmod(IMAGE_PATH, 0777)
                image_src = IMAGE_PATH + roll + '.png'
                f = open(image_src, 'w')
                f.write(profile.read())
                f.close()
                s3_path = 'profileimages/' + roll
                s3_link = copy_contents_to_s3_public(s3_path, image_src)
                Students.objects.create(
                    name=name, roll=roll, room=room,
                    email=email, mobile=mobile,
                    password=password, profile=s3_link)
            else:
                raise Exception('Student already registered')
            self.response['res_str'] = "Data added"
            return send_200(self.response)
        except Exception as e:
            self.response['res_str'] = str(e)
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

    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        data = request.GET
        roll = data['roll']

        st = Students.objects.get(roll=roll)
        password = "123456"
        st.password = password
        st.save()

        email = "sandeep.sharma@happay.in"

        send_email(email, password)

        self.response['res_str'] = "Link sent"
        return send_200(self.response)

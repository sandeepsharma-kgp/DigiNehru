# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render
from .models import Students
from .constants import ACTIVE, INACTIVE
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives, get_connection
from django.utils.crypto import get_random_string
from DigiNehruPy.settings import (EMAIL_HOST, EMAIL_HOST_USER,
                                  EMAIL_HOST_PASSWORD,
                                  AWS_ACCESS_KEY_ID,
                                  AWS_SECRET_ACCESS_KEY,
                                  AWS_STORAGE_BUCKET_NAME,
                                  REGION_HOST)
from DigiNehruPy.server_config import PROJECT_PATH
from DigiNehruPy.server_config import S3_BUCKET
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from tasks import add
import hashlib
import json
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

    from_email = "diginehru@gmail.in"
    subject = "Change Password"
    to_email = email
    to = [to_email]
    email_text = "Your password changed to: " + \
        password + " \nUse this password to reset to new one."
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
        password = hashlib.sha256(password).hexdigest()

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
        password = hashlib.sha256(password).hexdigest()
        # profile = file['profile']
        # add.apply_async(args=[])

        st = None
        try:
            st = Students.objects.get(roll=roll)
        except:
            pass

        if st and not st.status:
            self.update(data, st)
        try:
            if not st:
                # # print "in generate image url"
                # if not os.path.exists(IMAGE_PATH):
                #     os.makedirs(IMAGE_PATH)
                #     os.chmod(IMAGE_PATH, 0777)
                # image_src = IMAGE_PATH + roll + '.png'
                # f = open(image_src, 'w')
                # f.write(profile.read())
                # f.close()
                # s3_path = 'profileimages/' + roll
                # s3_link = copy_contents_to_s3_public(s3_path, image_src)
                # Students.objects.create(
                #     name=name, roll=roll, room=room,
                #     email=email, mobile=mobile,
                #     password=password, profile=s3_link)
                Students.objects.create(
                    name=name, roll=roll, room=room,
                    email=email, mobile=mobile,
                    password=password)
            else:
                self.response['res_str'] = "Student already registered"
                return send_400(self.response)
            self.response['res_str'] = "Registration Done!!"
            return send_200(self.response)
        except Exception as e:
            self.response['res_str'] = "Something went wrong!"
            import traceback
            error_msg = {}
            error_msg["TRACEBACK"] = traceback.format_exc()
            error_msg["ID"] = roll
            error_msg = json.dumps(error_msg)
            send_error_email(error_msg)
            return send_400(self.response)


class StudentLogin(View):

    def __init__(self):
        self.response = init_response()

    def post(self, request, *args, **kwargs):
        data = request.POST
        roll = data['roll']
        password = data['password']
        password = hashlib.sha256(password).hexdigest()

        try:
            st = Students.objects.get(roll=roll, password=password)
        except:
            st = None

        if st:
            if st.status == INACTIVE:
                self.response['res_str'] = "Account has been purged!!\
                                            \nContact: diginehru@gmail.com"
                return send_400(self.response)
            # st.token = uuid.uuid1()
            # st.save()
            self.response['res_str'] = "student-detail"
            self.response['res_data'] = st.serializer()
            return send_200(self.response)
        else:
            self.response['res_str'] = "Not Registered or Invalid Roll No./Password"
            # import traceback
            # error_msg = {}
            # error_msg["TRACEBACK"] = traceback.format_exc()
            # error_msg["ID"] = roll
            # error_msg = json.dumps(error_msg)
            # send_error_email(error_msg)
            return send_400(self.response)


class ForgotPassword(View):

    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        data = request.GET
        roll = data['roll']
        try:
            st = Students.objects.get(roll=roll)
        except:
            self.response['res_str'] = "Not Registered or Invalid Roll No."
            return send_400(self.response)

        password = get_random_string(length=6, allowed_chars='1234567890ABCDEF')
        save_password = hashlib.md5(password).hexdigest()
        save_password = hashlib.sha256(save_password).hexdigest()
        st.password = save_password
        st.save()

        email = st.email
        try:
            send_email(email, password)
        except:
            import traceback
            error_msg = {}
            error_msg["TRACEBACK"] = traceback.format_exc()
            error_msg["ID"] = s.roll
            error_msg = json.dumps(error_msg)
            send_error_email(error_msg, "Password-Forgot-Error")

        self.response['res_str'] = "Password sent to your registered e-mail id!"
        return send_200(self.response)

    def post(self, request, *args, **kwargs):
        data = request.POST
        roll = data['roll']
        prevpass = data['prevpass']
        prevpass = hashlib.sha256(prevpass).hexdigest()
        password = data['password']
        password = hashlib.sha256(password).hexdigest()

        try:
            st = Students.objects.get(roll=roll, password=prevpass)
        except:
            self.response['res_str'] = "Not Registered or Invalid Roll No./Password"
            return send_400(self.response)

        st.password = password
        st.save()

        self.response['res_str'] = "Your password is changed!"
        return send_200(self.response)

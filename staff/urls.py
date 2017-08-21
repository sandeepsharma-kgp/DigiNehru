from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    url(r'^staffregister/$', csrf_exempt(views.StaffSignUp.as_view()),
        name='staff-registration'),
    url(r'^stafflogin/$', csrf_exempt(views.StaffLogin.as_view()),
        name='staff-login'),
    url(r'^staffforgot/$', csrf_exempt(views.StaffLogin.as_view()),
        name='staff-forgot'),
]

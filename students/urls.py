from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    url(r'^$', views.login),
    url(r'^(?P<roll>[\w{}.-]{1,9})/$', views.login_id),
    url(r'^detail/(?P<roll>[\w{}.-]{1,9})/$',
        csrf_exempt(views.StudentLogin.as_view()), name='student-login')	,
    url(r'^studentregister/$', csrf_exempt(views.StudentSignUp.as_view()),
        name='student-registration'),
    url(r'^studentlogin/$',
        csrf_exempt(views.StudentLogin.as_view()), name='student-login'),
    url(r'^studentforgot/$',
        views.ForgotPassword.as_view(), name='student-forgot'),
]

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    url(r'^foodentry/$',
        csrf_exempt(views.StudentMenuEntry.as_view()),
        name='student-food-entry'),
]

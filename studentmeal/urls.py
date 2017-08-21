from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    url(r'^foodentry/$',
        csrf_exempt(views.StudentMenuEntry.as_view()),
        name='student-food-entry'),
    url(r'^mealcount/$',
        csrf_exempt(views.MealCount.as_view()),
        name='meal-count'),
]

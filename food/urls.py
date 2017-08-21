from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    url(r'^foodentry/$',
        csrf_exempt(views.FoodEntry.as_view()), name='food-entry'),
    url(r'^menuentry/$',
        csrf_exempt(views.MenuEntry.as_view()), name='menu-entry'),
    url(r'^foodtype/$',
        csrf_exempt(views.FoodTypeName.as_view()), name='type-entry'),
]

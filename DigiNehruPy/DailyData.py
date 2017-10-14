from studentmeal.models import mealcount
from students.models import Students
from datetime import datetime
import pytz
datetime.now(pytz.utc).date()
print "Registered Students: ", Students.objects.filter(status='1').count()
print "Lunch: " ,mealcount.objects.filter(eating_on=datetime.now(pytz.utc).date(),meals_taken__icontains='1').count()
print "Dinner: " ,mealcount.objects.filter(eating_on=datetime.now(pytz.utc).date(),meals_taken__icontains='3').count()
print "Breakfast: " ,mealcount.objects.filter(eating_on=datetime.now(pytz.utc).date(),meals_taken__icontains='0').count()
print "Snacks: " ,mealcount.objects.filter(eating_on=datetime.now(pytz.utc).date(),meals_taken__icontains='2').count()
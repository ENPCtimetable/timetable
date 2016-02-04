from django.http import HttpResponse
from django.shortcuts import render
import time

from date_time.views import create_day

def home(request):
    
    #Variables liées au template et a l'application day_time
    id_day = time.localtime()[6]+1
    day_list=create_day(id_day)[0]
    color=create_day(id_day)[1]
    user_firstname=create_day(id_day)[2]
    user_lastname=create_day(id_day)[3]
    day=create_day(id_day)[4]
    id_day=create_day(id_day)[5]

    #Variables liées a l'application room_available


    return render(request, 'custom_timetable/custom_timetable.html', locals()) #return HttpResponse(text)   
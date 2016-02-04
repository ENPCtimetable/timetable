from django.http import HttpResponse
from django.shortcuts import render
import datetime
import time

from date_time.views import create_day
from room_available.forms import ContactForm
import timetable.extract 

def delta(end):
    now = datetime.datetime.now()
    hour_delta = datetime.timedelta(hours=now.hour,minutes=now.minute)            
    end_delta = datetime.timedelta(hours=end.hour,minutes=end.minute)
    delta_second = end_delta - hour_delta
    delta = int(delta_second.seconds/(60*15))
    time_available = "| "*delta
    if end.minute < 10:
        str_minute = "0" + str(end.minute)
    else:
        str_minute = str(end.minute)
    if end.hour < 10:
         str_hour = "0" + str(end.hour)
    else:
        str_hour = str(end.hour)
    end_time = str_hour + ":" + str_minute
    return(time_available + end_time)


def home(request):
    "COMMENT FAIRE POUR EVITER DE COPIER LE CODE CI DESSOUS DANS CHAQUE FONCTION DE VUES CONTENANT DATETIME ?"
    
    #Variables liées au template et a l'application day_time
    id_day = time.localtime()[6]+1
    day_list=create_day(id_day)[0]
    color=create_day(id_day)[1]
    user_firstname=create_day(id_day)[2]
    user_lastname=create_day(id_day)[3]
    day=create_day(id_day)[4]
    id_day=create_day(id_day)[5]

    #Variables liées a l'application room_available
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = ContactForm(request.POST)  # Nous reprenons les données
        if form.is_valid(): # Nous vérifions que les données envoyées sont valides
            # Ici nous pouvons traiter les données du formulaire
            salle1 = form.cleaned_data['salle1']
            salle2 = form.cleaned_data['salle2']
            salle3 = form.cleaned_data['salle3']
            salle4 = form.cleaned_data['salle4']
            # Nous pourrions ici envoyer l'e-mail grâce aux données que nous venons de récupérer
            envoi = True
            room_type = form.display(salle1,salle2,salle3,salle4)

            dispo = timetable.extract.importation()
            room_name = dispo[room_type][0][0]
            end = dispo[room_type][0][3][1]
            dispo_time = delta(end)
            
    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = ContactForm()  # Nous créons un formulaire vide
        
    return render(request, 'room_available/room_available.html', locals()) 

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from datetime import datetime
import time

def home(request):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    text = """<h1>Ca gère</h1>
              <p>On est sur la vue du date_time !</p>"""
    return HttpResponse(text)

def choose_day(request):
    """ 
    Vue qui permet de retrouver le jour d'aujourd'hui 
    et de transmettre l'info à la fonction view_day
    """
    t = time.localtime()[6]+1
    return redirect(view_day, id_day=t)


def create_day(id_day):
    # Test for id_day
    if int(id_day) > 100 :
        return redirect(view_redirection)
    if int(id_day) < 1 or int(id_day) > 7 :
        raise Http404
    # Test for id_day
    day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    color=["Black"]*7
    color[int(id_day)-1] = "Red"
    day = day_list[int(id_day)-1] + " !"

    user_firstname="Réda"
    user_lastname="OUSSENNAN"

    return (day_list,color,user_firstname,user_lastname,day,id_day)


def view_day(request, id_day):
    """ 
    Vue qui affiche un jour selon son identifiant (ou ID, ici un numéro)
    Son ID est le second paramètre de la fonction (pour rappel, le premier
    paramètre est TOUJOURS la requête de l'utilisateur)
    """
    day_list=create_day(id_day)[0]
    color=create_day(id_day)[1]
    user_firstname=create_day(id_day)[2]
    user_lastname=create_day(id_day)[3]
    day=create_day(id_day)[4]

    return render(request, 'date_time/date_time.html', locals()) #return HttpResponse(text)       

def view_redirection(request):
    return redirect(home)

def view_date(request, id_day):
    day = datetime.now()
    list=["AA","BB"]

    day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dict_var={}

    for i in range(6) :
        key = day_list[i] 
        dict_var[key] = "Black"
    key = day_list[int(id_day)]
    dict_var[key] = "Red"

    return render(request, 'date_time/date_time.html', locals())
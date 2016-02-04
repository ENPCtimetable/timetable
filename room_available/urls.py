from django.conf.urls import patterns, url

urlpatterns = patterns('room_available.views',
    url(r'^accueil$', 'home'),
)
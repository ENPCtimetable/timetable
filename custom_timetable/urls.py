from django.conf.urls import patterns, url

urlpatterns = patterns('custom_timetable.views',
    url(r'^accueil$', 'home'),
)
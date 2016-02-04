from django.conf.urls import patterns, url

urlpatterns = patterns('date_time.views',
    url(r'^accueil$', 'home'),
    url(r'^which_day$', 'choose_day'),
    url(r'^(?P<id_day>\d+)$', 'view_day'), # Vue d'un jour particulier
    url(r'^redirection$', 'view_redirection'),
    url(r'^today(?P<id_day>\d+)$', 'view_date'),
)

